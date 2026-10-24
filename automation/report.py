"""What a run did, read from the ledger: likes sent, cards passed with the reason, messages per template and the reply rate of each template.

A row is {ts, action: like|pass|message|reply|run, live, profile, reason, template_id, text}. A `reply` row means the other side answered a conversation
this tool opened; its template_id is the opener it answered. Dry-run rows (live false) are listed apart so a plan is never counted as activity.
"""
import collections


def summarise(rows):
    live = [r for r in rows if r.get("live")]
    dry = [r for r in rows if not r.get("live") and r.get("action") in ("like", "pass", "message")]
    likes = [r for r in live if r.get("action") == "like"]
    passes = [r for r in rows if r.get("action") == "pass"]
    sent = [r for r in live if r.get("action") == "message"]
    replies = [r for r in live if r.get("action") == "reply"]
    by_reason = collections.Counter(r.get("reason", "?") for r in passes)
    per_template = {}
    for r in sent:
        per_template.setdefault(r.get("template_id", "?"), {"sent": 0, "replied": 0})["sent"] += 1
    answered = set()
    for r in replies:
        key = (r.get("profile", {}).get("name"), r.get("template_id"))
        if key not in answered and r.get("template_id") in per_template:
            answered.add(key)
            per_template[r["template_id"]]["replied"] += 1
    for stats in per_template.values():
        stats["reply_rate"] = round(stats["replied"] / stats["sent"], 2) if stats["sent"] else 0.0
    return {"likes": len(likes), "passes": len(passes), "messages": len(sent), "replies": len(answered), "dry_run_actions": len(dry),
            "pass_reasons": dict(by_reason), "templates": per_template}


def render_markdown(summary):
    lines = ["# ChatDaters automation report", "",
             "Likes sent: %d. Cards passed: %d. First messages sent: %d. Conversations answered: %d. Dry-run actions (planned, not done): %d." % (
                 summary["likes"], summary["passes"], summary["messages"], summary["replies"], summary["dry_run_actions"]), ""]
    if summary["pass_reasons"]:
        lines += ["## Why cards were passed", ""] + ["- %s: %d" % (k, v) for k, v in sorted(summary["pass_reasons"].items())] + [""]
    if summary["templates"]:
        lines += ["## Templates", "", "| Template | Sent | Answered | Reply rate |", "|---|---|---|---|"]
        for tid, s in sorted(summary["templates"].items()):
            lines.append("| %s | %d | %d | %d%% |" % (tid, s["sent"], s["replied"], round(s["reply_rate"] * 100)))
        lines.append("")
    return "\n".join(lines)
