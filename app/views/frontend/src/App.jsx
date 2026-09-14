import { useState } from "react";

const menu = [
  ["⌂", "Dashboard"], ["▤", "Orçamentos"], ["▧", "Ordens de Serviço"],
  ["▱", "Veículos"], ["♙", "Clientes"], ["▦", "Agenda"], ["⚒", "Serviços"],
  ["▫", "Peças / Estoque"], ["♙", "Funcionários"], ["ⓢ", "Financeiro"],
  ["▥", "Relatórios"], ["⚙", "Configurações"],
];

function App() {
  const [paginaAtual, setPaginaAtual] = useState("Dashboard");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark">⚙</div><div><strong>Oficina<span>Pro</span></strong><small>Sistema Interno</small></div></div>
        <nav aria-label="Menu principal">{menu.map(([icone, nome]) => <button className={paginaAtual === nome ? "ativo" : ""} onClick={() => setPaginaAtual(nome)} key={nome} type="button"><i aria-hidden="true">{icone}</i>{nome}</button>)}</nav>
        <div className="perfil"><div className="avatar">GJ</div><div><strong>Gabriel Jesus</strong><small>Administrador</small></div><span>⌄</span></div>
        <button className="sair" type="button">↪ <span>Sair do sistema</span></button>
      </aside>
      <main className="content"><header className="topbar"><button className="menu-toggle" type="button" aria-label="Abrir menu">☰</button><div className="search"><input placeholder="Buscar cliente, veículo, OS..." aria-label="Buscar"/><span>⌕</span></div><button className="bell" type="button" aria-label="Notificações">♧<b>3</b></button></header>
        <section className="empty-page"><div className="empty-icon">{menu.find(([_, nome]) => nome === paginaAtual)?.[0]}</div><h1>Hello, {paginaAtual}</h1><p>Esta é a página de {paginaAtual.toLowerCase()}.</p></section>
        <footer>© 2024 OficinaPro - Sistema Interno para Oficinas Mecânicas</footer>
      </main>
    </div>
  );
}

export default App;
