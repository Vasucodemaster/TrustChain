import { useEffect, useMemo, useState } from "react";
import "./App.css";

const NAV = [
  { id: "overview", code: "00", label: "Overview" },
  { id: "contributors", code: "ID", label: "Contributors" },
  { id: "analysis", code: "F4", label: "AI Analysis" },
  { id: "temporal", code: "F2", label: "Temporal Anomaly" },
  { id: "zk", code: "F3", label: "ZK Verification" },
  { id: "sybil", code: "F5", label: "Sybil Detection" },
  { id: "reputation", code: "F6", label: "Dynamic Reputation" },
];

const T = 75;

const CONTRIBUTORS = [
  {
    id: "c001",
    name: "Contributor 001",
    handle: "lab.alpha / core",
    trust: 92.4,
    quality: 91,
    code: 92,
    research: 86,
    docs: 89,
    risk: "LOW",
    status: "Verified",
    spike: "None",
    window: "90d",
    cluster: "C-01",
    proof: "valid",
  },
  {
    id: "c002",
    name: "Contributor 002",
    handle: "lab.beta / papers",
    trust: 87.4,
    quality: 88,
    code: 84,
    research: 91,
    docs: 86,
    risk: "LOW",
    status: "Verified",
    spike: "None",
    window: "90d",
    cluster: "C-01",
    proof: "valid",
  },
  {
    id: "c003",
    name: "Contributor 003",
    handle: "lab.gamma / reviews",
    trust: 81.7,
    quality: 84,
    code: 80,
    research: 82,
    docs: 88,
    risk: "LOW",
    status: "Verified",
    spike: "Mild",
    window: "60d",
    cluster: "C-02",
    proof: "valid",
  },
  {
    id: "c101",
    name: "Contributor 101",
    handle: "unknown / burst",
    trust: 42.1,
    quality: 39,
    code: 41,
    research: 36,
    docs: 33,
    risk: "HIGH",
    status: "Review",
    spike: "Commit burst +340%",
    window: "14d",
    cluster: "S-12",
    proof: "blocked",
  },
  {
    id: "c102",
    name: "Contributor 102",
    handle: "ring.node / alias",
    trust: 38.6,
    quality: 35,
    code: 38,
    research: 32,
    docs: 30,
    risk: "HIGH",
    status: "Review",
    spike: "Review ring",
    window: "30d",
    cluster: "S-12",
    proof: "blocked",
  },
  {
    id: "c103",
    name: "Contributor 103",
    handle: "sybil.edge / clone",
    trust: 35.2,
    quality: 31,
    code: 29,
    research: 34,
    docs: 28,
    risk: "HIGH",
    status: "Review",
    spike: "Identity fan-out",
    window: "21d",
    cluster: "S-04",
    proof: "blocked",
  },
];

function grade(score) {
  if (score >= 85) return "Excellent";
  if (score >= T) return "Pass";
  return "Hold";
}

function Pill({ tone, children }) {
  return <span className={`pill pill-${tone}`}>{children}</span>;
}

function PageTitle({ kicker, title, subtitle, extra }) {
  return (
    <header className="page-title">
      <div>
        {kicker ? <p className="page-kicker">{kicker}</p> : null}
        <h2>{title}</h2>
        {subtitle ? <p>{subtitle}</p> : null}
      </div>
      {extra}
    </header>
  );
}

function DataTable({ columns, rows, selectedId, onSelect }) {
  return (
    <div className="table-wrap">
      <div className="data-table" style={{ "--cols": columns.length }}>
        <div className="thead">
          {columns.map((c) => (
            <span key={c.key}>{c.label}</span>
          ))}
        </div>
        {rows.map((row) => (
          <button
            type="button"
            className={`trow${selectedId === row.id ? " is-selected" : ""}`}
            key={row.id}
            onClick={() => onSelect?.(row)}
          >
            {columns.map((c) => (
              <span key={c.key} className={c.className || ""}>
                {c.render ? c.render(row) : row[c.key]}
              </span>
            ))}
          </button>
        ))}
      </div>
    </div>
  );
}

function Inspector({ person, onClose, onOpen, onProve }) {
  if (!person) return null;
  const cleared = person.risk === "LOW" && person.quality >= T;
  return (
    <aside className="drawer">
      <div className="drawer-head">
        <div>
          <p className="page-kicker">Inspector</p>
          <h3>{person.name}</h3>
          <p className="dim">{person.handle}</p>
        </div>
        <button className="btn-ghost" type="button" onClick={onClose}>
          Close
        </button>
      </div>
      <div className="drawer-grid">
        <div>
          <span>Trust</span>
          <strong>{person.trust.toFixed(1)}</strong>
        </div>
        <div>
          <span>Quality</span>
          <strong>{person.quality}</strong>
        </div>
        <div>
          <span>Risk</span>
          <strong>{person.risk}</strong>
        </div>
        <div>
          <span>Proof</span>
          <strong>{person.proof}</strong>
        </div>
      </div>
      <p className="drawer-note">
        {cleared
          ? "Cleared for zk threshold proof and ERC-5114 mint."
          : "Issuance blocked. Graph clearance or substance score failed."}
      </p>
      <div className="drawer-actions">
        <button className="btn-primary" type="button" onClick={() => onOpen("analysis")}>
          Open analysis
        </button>
        <button className="btn-ghost" type="button" onClick={() => onProve(person)}>
          Simulate proof
        </button>
      </div>
    </aside>
  );
}

function OverviewPage({ people, selected, onSelect }) {
  const cleared = people.filter((c) => c.status === "Verified").length;
  const blocked = people.length - cleared;
  return (
    <>
      <PageTitle
        kicker="00 · TrustChain core"
        title="Issuance control room"
        subtitle="One path: private score → federated DP → temporal / Sybil clearance → zk proof score ≥ T → soulbound mint. GitHub is a case study."
      />
      <div className="stat-grid">
        <div className="stat">
          <span>Watched identities</span>
          <strong>{people.length}</strong>
        </div>
        <div className="stat good">
          <span>Cleared</span>
          <strong>{cleared}</strong>
        </div>
        <div className="stat bad">
          <span>Held</span>
          <strong>{blocked}</strong>
        </div>
        <div className="stat">
          <span>Public threshold T</span>
          <strong>{T}</strong>
        </div>
      </div>
      <ol className="pipeline">
        {[
          "Private evidence",
          "CodeBERT + SciBERT",
          "Flower + Opacus",
          "EvolveGCN / DySAT",
          "GraphSAGE",
          "Circom proof",
          "ERC-5114 mint",
        ].map((step, i) => (
          <li key={step}>
            <em>{String(i + 1).padStart(2, "0")}</em>
            {step}
          </li>
        ))}
      </ol>
      <DataTable
        selectedId={selected?.id}
        onSelect={onSelect}
        rows={people}
        columns={[
          { key: "name", label: "Contributor", className: "cell-name" },
          { key: "trust", label: "Trust", className: "cell-num", render: (r) => r.trust.toFixed(1) },
          { key: "quality", label: "AI Quality", className: "cell-num" },
          {
            key: "risk",
            label: "Risk",
            render: (r) => <Pill tone={r.risk === "LOW" ? "ok" : "risk"}>{r.risk}</Pill>,
          },
          { key: "status", label: "Status", render: (r) => <span className="linkish">{r.status}</span> },
        ]}
      />
    </>
  );
}

function ContributorsPage({ people, selected, onSelect, query, setQuery, risk, setRisk }) {
  const rows = people.filter((p) => {
    const q = query.trim().toLowerCase();
    const hit = !q || p.name.toLowerCase().includes(q) || p.handle.toLowerCase().includes(q);
    const rk = risk === "ALL" || p.risk === risk;
    return hit && rk;
  });
  return (
    <>
      <PageTitle
        kicker="ID · Registry"
        title="Contributors"
        extra={
          <div className="toolbar">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Filter identity or lab"
            />
            {["ALL", "LOW", "HIGH"].map((r) => (
              <button
                key={r}
                type="button"
                className={`chip${risk === r ? " is-on" : ""}`}
                onClick={() => setRisk(r)}
              >
                {r}
              </button>
            ))}
          </div>
        }
      />
      <DataTable
        selectedId={selected?.id}
        onSelect={onSelect}
        rows={rows}
        columns={[
          { key: "name", label: "Contributor", className: "cell-name", render: (r) => (
            <span>
              {r.name}
              <small className="dim"> {r.handle}</small>
            </span>
          ) },
          { key: "trust", label: "Trust", className: "cell-num", render: (r) => r.trust.toFixed(1) },
          { key: "quality", label: "AI Quality", className: "cell-num" },
          {
            key: "risk",
            label: "Risk",
            render: (r) => <Pill tone={r.risk === "LOW" ? "ok" : "risk"}>{r.risk}</Pill>,
          },
          { key: "status", label: "Status", render: (r) => r.status },
        ]}
      />
    </>
  );
}

function AnalysisPage({ person }) {
  const signals = [
    { label: "Code quality", value: person.code },
    { label: "Research value", value: person.research },
    { label: "Documentation", value: person.docs },
  ];
  return (
    <section className="panel ai-workspace">
      <PageTitle
        kicker="F4 · CodeBERT / SciBERT"
        title="AI contribution quality"
        subtitle={`${person.name} · multi-signal substance score. Count-based reputation is not used.`}
      />
      <div className="ai-hero">
        <div className="ai-hero-score">
          <span>Quality score</span>
          <strong>
            {person.quality}
            <em>/100</em>
          </strong>
        </div>
        <dl className="ai-meta">
          <div>
            <dt>Model</dt>
            <dd>CodeBERT / SciBERT</dd>
          </div>
          <div>
            <dt>Threshold T</dt>
            <dd>{T}</dd>
          </div>
          <div>
            <dt>Confidence</dt>
            <dd>{person.quality >= 80 ? "High" : "Low"}</dd>
          </div>
          <div>
            <dt>Assessment</dt>
            <dd>
              <Pill tone={person.quality >= T ? "ok" : "risk"}>{grade(person.quality)}</Pill>
            </dd>
          </div>
        </dl>
      </div>
      <div className="signal-list">
        {signals.map((s) => (
          <div className="signal-row" key={s.label}>
            <span>{s.label}</span>
            <div className="bar">
              <i style={{ width: `${s.value}%` }} />
            </div>
            <strong>{s.value}%</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function TemporalPage({ people, selected, onSelect }) {
  return (
    <>
      <PageTitle
        kicker="F2 · EvolveGCN / DySAT"
        title="Temporal anomaly"
        subtitle="Reputation-inflation spikes fail-close issuance before a proof is generated."
      />
      <DataTable
        selectedId={selected?.id}
        onSelect={onSelect}
        rows={people}
        columns={[
          { key: "name", label: "Contributor", className: "cell-name" },
          { key: "spike", label: "Signal" },
          { key: "window", label: "Window", className: "cell-num" },
          {
            key: "flag",
            label: "Flag",
            render: (r) => (
              <Pill tone={r.spike === "None" ? "ok" : "risk"}>
                {r.spike === "None" ? "Clear" : "Hold"}
              </Pill>
            ),
          },
          { key: "status", label: "Status" },
        ]}
      />
    </>
  );
}

function ZkPage({ person, log, onProve }) {
  const ready = person.risk === "LOW" && person.quality >= T && person.spike === "None";
  return (
    <>
      <PageTitle
        kicker="F3 · Circom + SnarkJS"
        title="Zero-knowledge threshold"
        subtitle="Prove committed score ≥ T without revealing the score. No mint unless the graph is clear."
      />
      <div className="stat-grid">
        <div className="stat">
          <span>Subject</span>
          <strong className="tiny">{person.name}</strong>
        </div>
        <div className="stat">
          <span>Public T</span>
          <strong>{T}</strong>
        </div>
        <div className="stat">
          <span>Circuit</span>
          <strong className="tiny">Groth16</strong>
        </div>
        <div className={`stat ${ready ? "good" : "bad"}`}>
          <span>Gate</span>
          <strong className="tiny">{ready ? "Ready" : "Blocked"}</strong>
        </div>
      </div>
      <div className="prove-box">
        <div>
          <p className="page-kicker">Issuance action</p>
          <h3>{ready ? "Generate threshold proof" : "Issuance refused"}</h3>
          <p className="dim">
            {ready
              ? "Graph cleared. Score stays on the institutional client. Only the proof goes on-chain."
              : "Fail closed: unapproved model, spike, Sybil cluster, or score below T."}
          </p>
        </div>
        <button className="btn-primary" type="button" disabled={!ready} onClick={() => onProve(person)}>
          {ready ? "Simulate Groth16 prove" : "Cannot mint"}
        </button>
      </div>
      <div className="log">
        {log.length === 0 ? (
          <p className="dim">No proofs this session.</p>
        ) : (
          log.map((e) => (
            <div key={e.ts} className="log-row">
              <span className="cell-num">{e.time}</span>
              <span className="cell-name">{e.name}</span>
              <span>{e.msg}</span>
            </div>
          ))
        )}
      </div>
    </>
  );
}

function SybilPage({ people, selected, onSelect }) {
  return (
    <>
      <PageTitle
        kicker="F5 · GraphSAGE"
        title="Sybil clusters"
        subtitle="Colluding identities share a cluster id. High-risk clusters cannot receive a soulbound badge."
      />
      <DataTable
        selectedId={selected?.id}
        onSelect={onSelect}
        rows={people}
        columns={[
          { key: "name", label: "Contributor", className: "cell-name" },
          { key: "cluster", label: "Cluster", className: "cell-num" },
          { key: "quality", label: "AI Quality", className: "cell-num" },
          {
            key: "risk",
            label: "Risk",
            render: (r) => <Pill tone={r.risk === "LOW" ? "ok" : "risk"}>{r.risk}</Pill>,
          },
          { key: "status", label: "Status" },
        ]}
      />
    </>
  );
}

export default function App() {
  const [view, setView] = useState("contributors");
  const [selectedId, setSelectedId] = useState(CONTRIBUTORS[0].id);
  const [query, setQuery] = useState("");
  const [risk, setRisk] = useState("ALL");
  const [drawer, setDrawer] = useState(false);
  const [log, setLog] = useState([]);
  const [clock, setClock] = useState(() => new Date());
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const id = setInterval(() => setClock(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (!toast) return undefined;
    const id = setTimeout(() => setToast(null), 2800);
    return () => clearTimeout(id);
  }, [toast]);

  const selected = useMemo(
    () => CONTRIBUTORS.find((c) => c.id === selectedId) || CONTRIBUTORS[0],
    [selectedId]
  );

  const select = (row) => {
    setSelectedId(row.id);
    setDrawer(true);
  };

  const prove = (person) => {
    const ok = person.risk === "LOW" && person.quality >= T && person.spike === "None";
    const entry = {
      ts: Date.now(),
      time: new Date().toLocaleTimeString(),
      name: person.name,
      msg: ok
        ? `Proof accepted · score ≥ ${T} · ERC-5114 ready on Polygon`
        : "Proof refused · fail-closed gate",
    };
    setLog((xs) => [entry, ...xs].slice(0, 8));
    setToast(entry.msg);
    setView("zk");
  };

  const page = {
    overview: (
      <OverviewPage people={CONTRIBUTORS} selected={selected} onSelect={select} />
    ),
    contributors: (
      <ContributorsPage
        people={CONTRIBUTORS}
        selected={selected}
        onSelect={select}
        query={query}
        setQuery={setQuery}
        risk={risk}
        setRisk={setRisk}
      />
    ),
    analysis: <AnalysisPage person={selected} />,
    temporal: <TemporalPage people={CONTRIBUTORS} selected={selected} onSelect={select} />,
    zk: <ZkPage person={selected} log={log} onProve={prove} />,
    sybil: <SybilPage people={CONTRIBUTORS} selected={selected} onSelect={select} />,
    reputation: <ReputationPage person={selected} />,
  }[view];

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" />
          <div>
            <strong>TrustChain</strong>
            <em>v0.1 prototype</em>
          </div>
        </div>
        <div className="sidebar-kicker">Intelligence modules</div>
        <nav className="sidebar-nav">
          {NAV.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`nav-item${view === item.id ? " active" : ""}`}
              onClick={() => setView(item.id)}
            >
              <span className="code">{item.code}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-foot">
          <span>Polygon Amoy</span>
          <span className="live">live session</span>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <span>Secure · explainable · privacy-aware contribution intelligence</span>
          <div className="topbar-right">
            <span className="mono">{clock.toLocaleTimeString()}</span>
            <span>System</span>
          </div>
        </header>
        <div className={`workspace-split${drawer ? " with-drawer" : ""}`}>
          <main className="content">{page}</main>
          {drawer ? (
            <Inspector
              person={selected}
              onClose={() => setDrawer(false)}
              onOpen={setView}
              onProve={prove}
            />
          ) : null}
        </div>
        <footer className="page-foot">
          <span>TrustChain · one issuance method · patent-style binding of O1–O6</span>
          <button className="text-btn" type="button" onClick={() => setDrawer(true)}>
            Inspect {selected.name}
          </button>
        </footer>
      </div>
      {toast ? <div className="toast">{toast}</div> : null}
    </div>
  );
}
