#!/usr/bin/env python3
"""Dependency-free control plane for the public Accelerator OS pack.

The CLI creates private-instance filesystem state, typed evidence, task envelopes,
and append-only events. It validates but never issues human approvals.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "accelerator"
REGISTRY_PATH = PACK / "registry" / "accelerator-os.json"

GATED_STATES = {"accepted", "rejected", "hold", "onboarding", "active", "graduated", "archived"}
TRANSITIONS = {
    "applied": {"consented", "archived"},
    "consented": {"normalized", "archived"},
    "normalized": {"screened", "archived"},
    "screened": {"diligence", "archived"},
    "diligence": {"ic_ready", "archived"},
    "ic_ready": {"accepted", "rejected", "hold", "archived"},
    "hold": {"diligence", "accepted", "rejected", "archived"},
    "accepted": {"onboarding", "archived"},
    "onboarding": {"active", "archived"},
    "active": {"graduated", "archived"},
    "graduated": {"archived"},
    "rejected": {"archived"},
    "archived": set(),
}
GATE_RULES = {
    "accepted": ("ic-decision", "approved"),
    "rejected": ("ic-decision", "rejected"),
    "hold": ("ic-decision", "hold"),
    "onboarding": ("company-onboarding", "approved"),
    "active": ("company-activation", "approved"),
    "graduated": ("company-graduation", "approved"),
    "archived": ("record-archive", "approved"),
}

STAGE_TASKS: dict[str, list[dict[str, Any]]] = {
    "consented": [{
        "agentId": "intake-analyst", "profileId": "evidence-lab",
        "objective": "Normalize the consented application and identify missing information.",
        "doneCondition": "Normalized intake, data-classification summary, and missing-information list exist.",
        "autonomyCeiling": "A2", "tools": ["file", "skills", "memory"],
        "evidence": ["consent-reference", "normalized-intake"],
    }],
    "normalized": [{
        "agentId": "thesis-fit-analyst", "profileId": "evidence-lab",
        "objective": "Map the normalized application to explicit program thesis criteria.",
        "doneCondition": "Fit matrix, disqualifiers, unknowns, and routing advice exist with evidence references.",
        "autonomyCeiling": "A2", "tools": ["file", "skills", "memory"],
        "evidence": ["program-thesis", "normalized-intake", "fit-matrix"],
    }],
    "screened": [
        {
            "agentId": agent, "profileId": "evidence-lab", "objective": objective,
            "doneCondition": "Source-backed observations, limitations, contradictions, and open questions are recorded.",
            "autonomyCeiling": "A2", "tools": ["web", "browser", "file", "skills", "memory"],
            "evidence": ["question-assignment", "evidence-records"],
        }
        for agent, objective in [
            ("market-researcher", "Collect public market and buyer evidence for the assigned questions."),
            ("product-analyst", "Assess product workflow, differentiation, adoption friction, and unknowns."),
            ("technical-analyst", "Assess authorized technical material and record implementation risks and unknowns."),
        ]
    ],
    "diligence": [{
        "agentId": "diligence-lead", "profileId": "program-director",
        "objective": "Assess evidence coverage and prepare the diligence packet for synthesis.",
        "doneCondition": "Coverage report, unresolved risks, falsifiers, and IC-readiness state exist.",
        "autonomyCeiling": "A2", "tools": ["kanban", "file", "skills", "memory"],
        "evidence": ["question-graph", "evidence-records", "coverage-report"],
    }],
    "accepted": [{
        "agentId": "onboarding-operator", "profileId": "program-director",
        "objective": "Prepare tenant-scoped onboarding after the human acceptance decision.",
        "doneCondition": "Tenant manifest draft, onboarding checklist, permission requests, and rollback owner exist.",
        "autonomyCeiling": "A2", "tools": ["kanban", "file", "skills", "memory"],
        "evidence": ["acceptance-receipt", "tenant-manifest-draft"],
    }],
    "onboarding": [{
        "agentId": "startup-os-architect", "profileId": "venture-builder",
        "objective": "Provision the smallest Day-0 Company OS and a bounded 30-day backlog.",
        "doneCondition": "Company OS manifest, 30-day backlog, isolation check, and rollback plan pass verification.",
        "autonomyCeiling": "A3", "tools": ["terminal", "file", "code_execution", "skills"],
        "evidence": ["onboarding-receipt", "company-os-manifest", "isolation-verdict"],
    }],
    "active": [{
        "agentId": "portfolio-health-analyst", "profileId": "portfolio-operator",
        "objective": "Open the first evidence-backed company review and support loop.",
        "doneCondition": "Company scorecard, top constraint, support route, cost baseline, and next proof event exist.",
        "autonomyCeiling": "A2", "tools": ["kanban", "file", "skills", "memory", "code_execution"],
        "evidence": ["activation-receipt", "company-scorecard"],
    }],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(program: Path, event: dict[str, Any]) -> None:
    with (program / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"ts": now(), **event}, ensure_ascii=False) + "\n")


def load_program(program: Path) -> dict[str, Any]:
    manifest = program / "program.json"
    if not manifest.exists():
        raise ValueError(f"not an Accelerator OS program: {program}")
    return load_json(manifest)


def application_path(program: Path, application_id: str) -> Path:
    safe_identifier(application_id, "application id")
    return program / "applications" / f"{application_id}.json"


def safe_identifier(value: str, label: str, allow_slash: bool = False) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    parts = value.split("/") if allow_slash else [value]
    if not value or any(
        not part or part in {".", ".."} or any(char not in allowed for char in part)
        for part in parts
    ):
        raise ValueError(f"{label} contains unsafe characters")
    return value


def evidence_path(program: Path, reference: str) -> Path:
    prefix = "evidence://"
    if not reference.startswith(prefix):
        raise ValueError(f"unsupported evidence reference: {reference}")
    evidence_id = safe_identifier(reference[len(prefix):], "evidence id", allow_slash=True)
    root = (program / "evidence").resolve()
    target = (root / f"{evidence_id}.json").resolve()
    if root not in target.parents:
        raise ValueError("evidence reference escapes the program evidence root")
    return target


def validate_evidence_refs(
    program: Path,
    program_data: dict[str, Any],
    application: dict[str, Any],
    references: list[str],
) -> None:
    for reference in references:
        path = evidence_path(program, reference)
        if not path.exists():
            raise ValueError(f"evidence record does not exist: {reference}")
        record = load_json(path)
        if record.get("schema") != "frankx.accelerator.evidence-record.v1":
            raise ValueError(f"evidence schema mismatch: {reference}")
        if record.get("institutionId") != program_data["institutionId"] or record.get("programId") != program_data["programId"]:
            raise ValueError(f"evidence tenant mismatch: {reference}")
        if record.get("companyId") != application.get("companyId"):
            raise ValueError(f"evidence company mismatch: {reference}")


def validate_receipt(
    path: Path,
    program_data: dict[str, Any],
    application: dict[str, Any],
    target_stage: str,
) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"approval receipt does not exist: {path}")
    receipt = load_json(path)
    required = {
        "schema", "id", "institutionId", "programId", "companyId", "gateId",
        "decision", "scope", "issuedBy", "issuedAt", "expiresAt", "artifactRefs",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        raise ValueError(f"approval receipt missing: {', '.join(missing)}")
    if receipt["schema"] != "frankx.accelerator.approval-receipt.v1":
        raise ValueError("approval receipt schema mismatch")
    safe_identifier(str(receipt["id"]), "approval receipt id")
    issuer = receipt.get("issuedBy", {})
    if not isinstance(issuer, dict) or issuer.get("type") != "human" or not issuer.get("name"):
        raise ValueError("approval receipt must be issued by a named human")
    if receipt["institutionId"] != program_data["institutionId"] or receipt["programId"] != program_data["programId"]:
        raise ValueError("approval receipt tenant mismatch")
    if not application.get("companyId") or receipt.get("companyId") != application["companyId"]:
        raise ValueError("approval receipt company mismatch")
    expected_gate, expected_decision = GATE_RULES[target_stage]
    if receipt["gateId"] != expected_gate or receipt["decision"] != expected_decision:
        raise ValueError(f"{target_stage} requires gate={expected_gate}, decision={expected_decision}")
    try:
        expires = datetime.fromisoformat(str(receipt["expiresAt"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("approval receipt expiresAt is invalid") from exc
    if expires.tzinfo is None:
        raise ValueError("approval receipt expiresAt must include a timezone")
    if expires <= datetime.now(timezone.utc):
        raise ValueError("approval receipt is expired")
    return receipt


def validate_verdict(
    path: Path,
    program_data: dict[str, Any],
    application: dict[str, Any],
) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"verifier verdict does not exist: {path}")
    verdict = load_json(path)
    required = {
        "schema", "id", "institutionId", "programId", "companyId", "artifactRef",
        "maker", "verifier", "verdict", "checks", "findings", "checkedAt",
    }
    missing = sorted(required - verdict.keys())
    if missing:
        raise ValueError(f"verifier verdict missing: {', '.join(missing)}")
    if verdict["schema"] != "frankx.accelerator.verifier-verdict.v1":
        raise ValueError("verifier verdict schema mismatch")
    safe_identifier(str(verdict["id"]), "verifier verdict id")
    if verdict["institutionId"] != program_data["institutionId"] or verdict["programId"] != program_data["programId"]:
        raise ValueError("verifier verdict tenant mismatch")
    if verdict["companyId"] != application.get("companyId"):
        raise ValueError("verifier verdict company mismatch")
    maker = verdict.get("maker")
    verifier = verdict.get("verifier")
    if not isinstance(maker, dict) or not isinstance(verifier, dict):
        raise ValueError("verifier verdict maker and verifier must be objects")
    if verifier.get("profileId") != "independent-verifier":
        raise ValueError("verifier verdict must use the independent-verifier profile")
    if maker.get("agentId") == verifier.get("agentId"):
        raise ValueError("maker and verifier agents must differ")
    if maker.get("provider") == verifier.get("provider"):
        raise ValueError("maker and verifier providers must differ")
    if verdict["verdict"] != "pass":
        raise ValueError("ic_ready requires a passing independent verifier verdict")
    return verdict


def create_tasks(program: Path, program_data: dict[str, Any], application: dict[str, Any], stage: str) -> list[str]:
    task_ids: list[str] = []
    for spec in STAGE_TASKS.get(stage, []):
        task_id = f"task-{stage}-{uuid.uuid4().hex[:10]}"
        task = {
            "schema": "frankx.accelerator.task-envelope.v1",
            "id": task_id,
            "institutionId": program_data["institutionId"],
            "programId": program_data["programId"],
            "companyId": application.get("companyId"),
            "workflow": "application-to-ic" if stage in {"consented", "normalized", "screened", "diligence"} else "accepted-to-day0",
            "stage": stage,
            "agentId": spec["agentId"],
            "profileId": spec["profileId"],
            "objective": spec["objective"],
            "doneCondition": spec["doneCondition"],
            "autonomyCeiling": spec["autonomyCeiling"],
            "allowedTools": spec["tools"],
            "writeScopes": [f"program/{program_data['programId']}", f"company/{application.get('companyId') or 'unassigned'}"],
            "inputRefs": [f"application://{application['applicationId']}"],
            "evidenceRequired": spec["evidence"],
            "requiredVerifierProfile": "independent-verifier",
            "approvalGateIds": [],
            "budget": {"maxMinutes": 90, "maxModelCost": 10, "currency": "EUR"},
            "status": "queued",
            "createdAt": now(),
            "deadline": None,
            "resultRefs": [],
        }
        write_json(program / "tasks" / f"{task_id}.json", task)
        task_ids.append(task_id)
        append_event(program, {
            "type": "task.created", "taskId": task_id,
            "applicationId": application["applicationId"], "stage": stage,
        })
    return task_ids


def validate_pack() -> list[str]:
    errors: list[str] = []
    required_paths = [
        PACK / "README.md", PACK / "RUNBOOK.md", REGISTRY_PATH,
        PACK / "schemas" / "task-envelope.schema.json",
        PACK / "schemas" / "evidence-record.schema.json",
        PACK / "schemas" / "approval-receipt.schema.json",
        PACK / "schemas" / "tenant-manifest.schema.json",
        PACK / "schemas" / "verifier-verdict.schema.json",
        PACK / "examples" / "synthetic-pilot-program.json",
        PACK / "examples" / "synthetic-application.json",
        PACK / "examples" / "synthetic-approval-receipt.json",
        PACK / "examples" / "synthetic-verifier-verdict.json",
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        return errors

    registry = load_json(REGISTRY_PATH)
    profiles = registry.get("profiles", [])
    agents = registry.get("agents", [])
    swarms = registry.get("swarms", [])
    if len(profiles) != 5:
        errors.append("registry must define exactly five runtime profiles")
    profile_ids = [item.get("id") for item in profiles]
    agent_ids = [item.get("id") for item in agents]
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("profile IDs must be unique")
    if len(agent_ids) != len(set(agent_ids)):
        errors.append("agent IDs must be unique")
    known_profiles = set(profile_ids)
    known_agents = set(agent_ids)
    profile_map = {item["id"]: item for item in profiles}
    agent_map = {item["id"]: item for item in agents}

    referenced_skills: set[str] = set()
    for agent in agents:
        if agent.get("profile") not in known_profiles:
            errors.append(f"agent {agent.get('id')} references unknown profile {agent.get('profile')}")
        referenced_skills.update(agent.get("skills", []))
    for swarm in swarms:
        for agent_id in [*swarm.get("agents", []), *swarm.get("assurance", [])]:
            if agent_id not in known_agents:
                errors.append(f"swarm {swarm.get('id')} references unknown agent {agent_id}")

    autonomy_order = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5}
    for stage, specs in STAGE_TASKS.items():
        for spec in specs:
            agent = agent_map.get(spec["agentId"])
            profile = profile_map.get(spec["profileId"])
            if not agent:
                errors.append(f"stage {stage} references unknown agent {spec['agentId']}")
                continue
            if not profile:
                errors.append(f"stage {stage} references unknown profile {spec['profileId']}")
                continue
            if agent.get("profile") != spec["profileId"]:
                errors.append(f"stage {stage} profile differs from registry for {spec['agentId']}")
            if not set(spec["tools"]).issubset(set(profile.get("toolsets", []))):
                errors.append(f"stage {stage} tools exceed profile allowance for {spec['agentId']}")
            if autonomy_order[spec["autonomyCeiling"]] > autonomy_order[profile["maxAutonomy"]]:
                errors.append(f"stage {stage} autonomy exceeds profile allowance for {spec['agentId']}")

    for skill in sorted(referenced_skills):
        skill_path = PACK / "skills" / skill / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"missing referenced skill accelerator/skills/{skill}/SKILL.md")
        elif f"name: {skill}" not in skill_path.read_text(encoding="utf-8"):
            errors.append(f"skill name mismatch in {skill_path.relative_to(ROOT)}")
    for schema in (PACK / "schemas").glob("*.json"):
        try:
            data = load_json(schema)
            if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"{schema.relative_to(ROOT)} is not draft 2020-12")
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {schema.relative_to(ROOT)}: {exc}")
    if set(registry.get("workflowStates", [])) != set(TRANSITIONS):
        errors.append("registry workflowStates and CLI state machine differ")
    if set(registry.get("gatedStates", [])) != GATED_STATES:
        errors.append("registry gatedStates and CLI gate rules differ")

    expected_examples = {
        "synthetic-pilot-program.json": "frankx.accelerator.pilot-program.v1",
        "synthetic-application.json": "frankx.accelerator.synthetic-application.v1",
        "synthetic-approval-receipt.json": "frankx.accelerator.approval-receipt.v1",
        "synthetic-verifier-verdict.json": "frankx.accelerator.verifier-verdict.v1",
    }
    for filename, expected_schema in expected_examples.items():
        example = load_json(PACK / "examples" / filename)
        if example.get("schema") != expected_schema:
            errors.append(f"example {filename} has the wrong schema")
    return errors


def command_validate(_: argparse.Namespace) -> int:
    errors = validate_pack()
    if errors:
        for error in errors:
            print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("Accelerator OS validation passed.")
    return 0


def command_init(args: argparse.Namespace) -> int:
    safe_identifier(args.institution_id, "institution id")
    safe_identifier(args.program_id, "program id")
    output = Path(args.output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be empty or absent: {output}")
    for directory in ["applications", "tasks", "evidence", "approvals", "companies", "verdicts"]:
        (output / directory).mkdir(parents=True, exist_ok=True)
    program = {
        "schema": "frankx.accelerator.program.v1",
        "institutionId": args.institution_id,
        "programId": args.program_id,
        "name": args.name,
        "status": "pilot",
        "registryRef": str(REGISTRY_PATH.relative_to(ROOT)).replace("\\", "/"),
        "dataPolicy": "Private instance: store only authorized tenant data; never commit runtime state to the public starter.",
        "createdAt": now(),
    }
    write_json(output / "program.json", program)
    append_event(output, {"type": "program.created", "institutionId": args.institution_id, "programId": args.program_id})
    print(output)
    return 0


def command_intake(args: argparse.Namespace) -> int:
    program_path = Path(args.program).resolve()
    program = load_program(program_path)
    safe_identifier(args.company_id or f"company-{args.application_id}", "company id")
    target = application_path(program_path, args.application_id)
    if target.exists():
        raise ValueError(f"application already exists: {args.application_id}")
    application = {
        "schema": "frankx.accelerator.application-state.v1",
        "institutionId": program["institutionId"],
        "programId": program["programId"],
        "applicationId": args.application_id,
        "companyId": args.company_id or f"company-{args.application_id}",
        "companyName": args.company,
        "source": args.source,
        "consentRef": args.consent_ref,
        "state": "consented",
        "stateHistory": [
            {"state": "applied", "at": now()},
            {"state": "consented", "at": now(), "evidenceRef": args.consent_ref},
        ],
        "evidenceRefs": [args.consent_ref],
        "approvalRefs": [],
        "verifierRefs": [],
        "taskRefs": [],
        "createdAt": now(),
        "updatedAt": now(),
    }
    write_json(target, application)
    append_event(program_path, {"type": "application.consented", "applicationId": args.application_id, "companyId": application["companyId"]})
    application["taskRefs"].extend(create_tasks(program_path, program, application, "consented"))
    application["updatedAt"] = now()
    write_json(target, application)
    print(json.dumps({"applicationId": args.application_id, "state": "consented", "tasks": application["taskRefs"]}, indent=2))
    return 0


def command_record_evidence(args: argparse.Namespace) -> int:
    program_path = Path(args.program).resolve()
    program = load_program(program_path)
    path = application_path(program_path, args.application_id)
    if not path.exists():
        raise ValueError(f"application not found: {args.application_id}")
    application = load_json(path)
    evidence_id = safe_identifier(args.evidence_id, "evidence id", allow_slash=True)
    reference = f"evidence://{evidence_id}"
    target = evidence_path(program_path, reference)
    if target.exists():
        raise ValueError(f"evidence record already exists: {reference}")
    if not 0 <= args.confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    record = {
        "schema": "frankx.accelerator.evidence-record.v1",
        "id": evidence_id,
        "institutionId": program["institutionId"],
        "programId": program["programId"],
        "companyId": application["companyId"],
        "claim": args.claim,
        "state": args.state,
        "source": {"type": args.source_type, "locator": args.source, "title": args.title},
        "observedAt": now(),
        "createdBy": args.created_by,
        "confidence": args.confidence,
        "limitations": args.limitation,
        "dataClass": args.data_class,
        "shareScope": "company",
        "createdAt": now(),
    }
    write_json(target, record)
    append_event(program_path, {
        "type": "evidence.recorded", "applicationId": args.application_id,
        "evidenceRef": reference, "createdBy": args.created_by,
    })
    print(json.dumps({"evidenceRef": reference, "path": str(target)}, indent=2))
    return 0


def command_advance(args: argparse.Namespace) -> int:
    program_path = Path(args.program).resolve()
    program = load_program(program_path)
    path = application_path(program_path, args.application_id)
    if not path.exists():
        raise ValueError(f"application not found: {args.application_id}")
    application = load_json(path)
    current = application["state"]
    target = args.stage
    if target not in TRANSITIONS.get(current, set()):
        raise ValueError(f"invalid transition: {current} -> {target}")

    approval_ref: str | None = None
    verifier_ref: str | None = None
    if target in GATED_STATES:
        if args.evidence:
            validate_evidence_refs(program_path, program, application, args.evidence)
        if not args.approval_file:
            raise ValueError(f"{target} is human-gated; --approval-file is required")
        receipt = validate_receipt(Path(args.approval_file).resolve(), program, application, target)
        approval_ref = f"approval://{receipt['id']}"
        destination = program_path / "approvals" / f"{receipt['id']}.json"
        if destination.exists():
            raise ValueError(f"approval receipt was already consumed: {receipt['id']}")
        write_json(destination, receipt)
        application.setdefault("approvalRefs", []).append(approval_ref)
    else:
        if not args.evidence:
            raise ValueError("ungated transitions require at least one --evidence reference")
        validate_evidence_refs(program_path, program, application, args.evidence)
        if target == "ic_ready":
            if not args.verifier_file:
                raise ValueError("ic_ready requires --verifier-file from an independent provider")
            verdict = validate_verdict(Path(args.verifier_file).resolve(), program, application)
            verifier_ref = f"verdict://{verdict['id']}"
            destination = program_path / "verdicts" / f"{verdict['id']}.json"
            if destination.exists():
                raise ValueError(f"verifier verdict was already consumed: {verdict['id']}")
            write_json(destination, verdict)
            application.setdefault("verifierRefs", []).append(verifier_ref)

    application["state"] = target
    application.setdefault("stateHistory", []).append({
        "state": target, "at": now(), "evidenceRefs": args.evidence,
        "approvalRef": approval_ref, "verifierRef": verifier_ref,
    })
    application.setdefault("evidenceRefs", []).extend(args.evidence)
    new_tasks = create_tasks(program_path, program, application, target)
    application.setdefault("taskRefs", []).extend(new_tasks)
    application["updatedAt"] = now()
    write_json(path, application)
    append_event(program_path, {
        "type": "application.state_changed", "applicationId": args.application_id,
        "from": current, "to": target, "evidenceRefs": args.evidence,
        "approvalRef": approval_ref, "verifierRef": verifier_ref,
    })
    print(json.dumps({"applicationId": args.application_id, "from": current, "to": target, "tasks": new_tasks}, indent=2))
    return 0


def command_status(args: argparse.Namespace) -> int:
    program_path = Path(args.program).resolve()
    program = load_program(program_path)
    applications = [load_json(path) for path in sorted((program_path / "applications").glob("*.json"))]
    tasks = [load_json(path) for path in sorted((program_path / "tasks").glob("*.json"))]
    application_states: dict[str, int] = {}
    for application in applications:
        application_states[application["state"]] = application_states.get(application["state"], 0) + 1
    task_states: dict[str, int] = {}
    for task in tasks:
        task_states[task["status"]] = task_states.get(task["status"], 0) + 1
    print(json.dumps({
        "institutionId": program["institutionId"], "programId": program["programId"],
        "applications": len(applications), "applicationStates": application_states,
        "tasks": len(tasks), "taskStates": task_states,
    }, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Accelerator OS local control plane")
    commands = root.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate the public Accelerator OS pack")
    validate.set_defaults(func=command_validate)

    init = commands.add_parser("init-program", help="create an isolated program runtime directory")
    init.add_argument("--institution-id", default="institution-local")
    init.add_argument("--program-id", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--output", required=True)
    init.set_defaults(func=command_init)

    intake = commands.add_parser("intake", help="create a consented application and intake task")
    intake.add_argument("--program", required=True)
    intake.add_argument("--application-id", required=True)
    intake.add_argument("--company-id")
    intake.add_argument("--company", required=True)
    intake.add_argument("--source", required=True)
    intake.add_argument("--consent-ref", required=True)
    intake.set_defaults(func=command_intake)

    evidence = commands.add_parser("record-evidence", help="write one typed tenant-scoped evidence record")
    evidence.add_argument("--program", required=True)
    evidence.add_argument("--application-id", required=True)
    evidence.add_argument("--evidence-id", required=True)
    evidence.add_argument("--claim", required=True)
    evidence.add_argument("--state", required=True, choices=["observed", "sourced", "founder_asserted", "inferred", "contradicted", "stale", "unknown"])
    evidence.add_argument("--source-type", required=True, choices=["primary-public", "secondary-public", "founder-supplied", "authorized-private", "experiment", "unknown"])
    evidence.add_argument("--source", required=True)
    evidence.add_argument("--title", required=True)
    evidence.add_argument("--created-by", required=True)
    evidence.add_argument("--confidence", type=float, required=True)
    evidence.add_argument("--limitation", action="append", default=[])
    evidence.add_argument("--data-class", required=True, choices=["public", "program-private", "company-private", "restricted"])
    evidence.set_defaults(func=command_record_evidence)

    advance = commands.add_parser("advance", help="advance one application through an allowed state transition")
    advance.add_argument("--program", required=True)
    advance.add_argument("--application-id", required=True)
    advance.add_argument("--stage", required=True, choices=sorted(TRANSITIONS))
    advance.add_argument("--evidence", action="append", default=[])
    advance.add_argument("--approval-file")
    advance.add_argument("--verifier-file")
    advance.set_defaults(func=command_advance)

    status = commands.add_parser("status", help="show program/application/task state")
    status.add_argument("--program", required=True)
    status.set_defaults(func=command_status)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"accelerator-os: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
