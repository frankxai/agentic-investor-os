#!/usr/bin/env python3
"""Tests for the dependency-free Accelerator OS control plane."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import accelerator_os


class AcceleratorOsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.program = Path(self.temp.name) / "program"
        self.quiet(
            accelerator_os.command_init,
            argparse.Namespace(
                institution_id="institution-synthetic",
                program_id="pilot-public-safe",
                name="Public Safe Pilot",
                output=str(self.program),
            ),
        )
        self.create_application()

    @staticmethod
    def quiet(function, args) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return function(args)

    def create_application(self, application_id: str = "app-001", company_id: str = "company-synthetic-studio") -> None:
        self.quiet(
            accelerator_os.command_intake,
            argparse.Namespace(
                program=str(self.program),
                application_id=application_id,
                company_id=company_id,
                company="Synthetic Studio",
                source="public-safe-test",
                consent_ref="consent://synthetic/demo-only",
            ),
        )

    def record_evidence(self, label: str, application_id: str = "app-001") -> str:
        evidence_id = f"{application_id}/{label}-v1"
        self.quiet(
            accelerator_os.command_record_evidence,
            argparse.Namespace(
                program=str(self.program),
                application_id=application_id,
                evidence_id=evidence_id,
                claim=f"Synthetic {label} evidence exists for state-machine testing.",
                state="observed",
                source_type="experiment",
                source=f"fixture://{application_id}/{label}",
                title=f"Synthetic {label} fixture",
                created_by="synthetic-test-agent",
                confidence=0.8,
                limitation=["Synthetic test data only"],
                data_class="company-private",
            ),
        )
        return f"evidence://{evidence_id}"

    def advance(
        self,
        stage: str,
        evidence: list[str] | None = None,
        approval_file: str | None = None,
        verifier_file: str | None = None,
        application_id: str = "app-001",
    ) -> int:
        return self.quiet(
            accelerator_os.command_advance,
            argparse.Namespace(
                program=str(self.program),
                application_id=application_id,
                stage=stage,
                evidence=evidence or [],
                approval_file=approval_file,
                verifier_file=verifier_file,
            ),
        )

    def reach_diligence(self, application_id: str = "app-001") -> None:
        for stage in ["normalized", "screened", "diligence"]:
            self.advance(stage, [self.record_evidence(stage, application_id)], application_id=application_id)

    def reach_ic_ready(self, application_id: str = "app-001") -> None:
        self.reach_diligence(application_id)
        verifier = accelerator_os.PACK / "examples" / "synthetic-verifier-verdict.json"
        self.advance(
            "ic_ready",
            [self.record_evidence("ic-ready", application_id)],
            verifier_file=str(verifier),
            application_id=application_id,
        )

    def application(self, application_id: str = "app-001") -> dict:
        return json.loads((self.program / "applications" / f"{application_id}.json").read_text(encoding="utf-8"))

    def write_fixture_copy(self, filename: str, updates: dict) -> Path:
        source = accelerator_os.PACK / "examples" / filename
        data = json.loads(source.read_text(encoding="utf-8"))
        data.update(updates)
        target = Path(self.temp.name) / f"modified-{filename}"
        target.write_text(json.dumps(data), encoding="utf-8")
        return target

    def test_pack_validates(self) -> None:
        self.assertEqual([], accelerator_os.validate_pack())

    def test_application_dispatches_tenant_scoped_tasks(self) -> None:
        self.reach_ic_ready()
        tasks = [json.loads(path.read_text(encoding="utf-8")) for path in (self.program / "tasks").glob("*.json")]
        self.assertEqual("ic_ready", self.application()["state"])
        self.assertEqual(6, len(tasks))
        self.assertTrue(all(task["institutionId"] == "institution-synthetic" for task in tasks))
        self.assertTrue(all(task["companyId"] == "company-synthetic-studio" for task in tasks))
        self.assertTrue(all(task["requiredVerifierProfile"] == "independent-verifier" for task in tasks))

    def test_missing_evidence_record_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "evidence record does not exist"):
            self.advance("normalized", ["evidence://app-001/missing"])

    def test_recorded_evidence_matches_published_schema_contract(self) -> None:
        reference = self.record_evidence("schema-contract")
        record = json.loads(accelerator_os.evidence_path(self.program, reference).read_text(encoding="utf-8"))
        schema = json.loads(
            (accelerator_os.PACK / "schemas" / "evidence-record.schema.json").read_text(encoding="utf-8")
        )
        self.assertTrue(set(schema["required"]).issubset(record))
        self.assertTrue(set(record).issubset(schema["properties"]))
        self.assertIn(record["state"], schema["properties"]["state"]["enum"])
        self.assertIn(record["source"]["type"], schema["properties"]["source"]["properties"]["type"]["enum"])
        self.assertIn(record["dataClass"], schema["properties"]["dataClass"]["enum"])

    def test_ic_ready_requires_different_provider_verifier(self) -> None:
        self.reach_diligence()
        verifier = self.write_fixture_copy(
            "synthetic-verifier-verdict.json",
            {
                "maker": {"agentId": "memo-editor", "provider": "same-provider"},
                "verifier": {
                    "agentId": "independent-verifier",
                    "profileId": "independent-verifier",
                    "provider": "same-provider",
                },
            },
        )
        with self.assertRaisesRegex(ValueError, "providers must differ"):
            self.advance("ic_ready", [self.record_evidence("ic-ready")], verifier_file=str(verifier))

    def test_human_gate_fails_closed_without_receipt(self) -> None:
        self.reach_ic_ready()
        with self.assertRaisesRegex(ValueError, "human-gated"):
            self.advance("accepted")
        self.assertEqual("ic_ready", self.application()["state"])

    def test_gated_transition_rejects_dangling_evidence(self) -> None:
        self.reach_ic_ready()
        fixture = accelerator_os.PACK / "examples" / "synthetic-approval-receipt.json"
        with self.assertRaisesRegex(ValueError, "evidence record does not exist"):
            self.advance("accepted", ["evidence://app-001/missing"], approval_file=str(fixture))
        self.assertEqual("ic_ready", self.application()["state"])

    def test_valid_synthetic_receipt_advances_and_dispatches_onboarding(self) -> None:
        self.reach_ic_ready()
        fixture = accelerator_os.PACK / "examples" / "synthetic-approval-receipt.json"
        self.advance("accepted", approval_file=str(fixture))
        application = self.application()
        self.assertEqual("accepted", application["state"])
        self.assertIn("approval://approval-synthetic-ic-001", application["approvalRefs"])
        tasks = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (self.program / "tasks").glob("task-accepted-*.json")
        ]
        self.assertEqual("onboarding-operator", tasks[0]["agentId"])

    def test_previously_consumed_receipt_is_rejected(self) -> None:
        self.reach_ic_ready()
        fixture = accelerator_os.PACK / "examples" / "synthetic-approval-receipt.json"
        destination = self.program / "approvals" / "approval-synthetic-ic-001.json"
        shutil.copyfile(fixture, destination)
        with self.assertRaisesRegex(ValueError, "already consumed"):
            self.advance("accepted", approval_file=str(fixture))

    def test_receipt_company_is_mandatory_and_exact(self) -> None:
        self.reach_ic_ready()
        receipt = self.write_fixture_copy("synthetic-approval-receipt.json", {"companyId": None})
        with self.assertRaisesRegex(ValueError, "company mismatch"):
            self.advance("accepted", approval_file=str(receipt))

    def test_naive_receipt_expiry_is_cleanly_rejected(self) -> None:
        self.reach_ic_ready()
        receipt = self.write_fixture_copy("synthetic-approval-receipt.json", {"expiresAt": "2099-01-01T00:00:00"})
        with self.assertRaisesRegex(ValueError, "must include a timezone"):
            self.advance("accepted", approval_file=str(receipt))

    def test_receipt_tenant_mismatch_is_rejected(self) -> None:
        self.reach_ic_ready()
        receipt = self.write_fixture_copy("synthetic-approval-receipt.json", {"programId": "another-program"})
        with self.assertRaisesRegex(ValueError, "tenant mismatch"):
            self.advance("accepted", approval_file=str(receipt))

    def test_invalid_transition_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid transition"):
            self.advance("active", ["evidence://invalid"])


if __name__ == "__main__":
    unittest.main()
