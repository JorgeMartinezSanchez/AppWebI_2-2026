// ============================================
// DATOS — edita esto para personalizar el contenido
// ============================================

const FETCH_INFO = [
  ["user", "jorge"],
  ["role", "Estudiante de Ingeniería de Software · UCB"],
  ["os", "Kubuntu (KDE Plasma)"],
  ["stack", "Full-stack · Sistemas · Contenedores"],
  ["shell", "kitty + Starship"],
  ["uptime", "aprendiendo desde el primer semestre"],
];

const PROJECTS = [
  {
    name: "residencial-al-cubo",
    title: "Residencial Al Cubo",
    desc: "API REST de gestión hotelera en ASP.NET Core con PostgreSQL, EF Core y patrones Repository/Service/State/Strategy. Desplegada en Railway.",
    tags: ["ASP.NET Core", "PostgreSQL", "EF Core", "Railway"],
  },
  {
    name: "mytherapist",
    title: "MyTherapist",
    desc: "App de agendamiento en Angular con backend en Supabase, integración de FullCalendar y pruebas unitarias con Jest.",
    tags: ["Angular", "Supabase", "FullCalendar", "Jest"],
  },
  {
    name: "safechat",
    title: "SafeChat",
    desc: "Chat cifrado con Angular + C#, MongoDB, y cifrado RSA/AES sobre una arquitectura basada en componentes.",
    tags: ["Angular", "C#", "MongoDB", "RSA/AES"],
  },
  {
    name: "loud",
    title: "LOUD — eventos y ticketing",
    desc: "Aplicación de venta de entradas con Docker Compose, PostgreSQL, Django, FastAPI, Nginx y JS vanilla.",
    tags: ["Docker", "Django", "FastAPI", "Nginx"],
  },
  {
    name: "os-exam-stack",
    title: "Stack de examen de SO",
    desc: "Proyecto de Sistemas Operativos con MySQL, PostgreSQL, Redis, Node.js, FastAPI y Vue.js, todo orquestado con Docker.",
    tags: ["Docker", "Redis", "Vue.js", "FastAPI"],
  },
  {
    name: "vinchuca-classifier",
    title: "Clasificador de vinchucas",
    desc: "Clasificador binario de imágenes en PyTorch (CNN propia, aumento de datos, early stopping) — AUC de 0.93.",
    tags: ["PyTorch", "CNN", "Visión por computadora"],
  },
];

const STACK = [
  {
    title: "lenguajes",
    items: ["JavaScript / TypeScript", "C# ", "Python", "SQL"],
  },
  {
    title: "frameworks",
    items: ["Angular", "Django", "FastAPI", "ASP.NET Core", "Web Components"],
  },
  {
    title: "infra",
    items: ["Docker / Compose", "Nginx", "PostgreSQL", "MongoDB", "Redis"],
  },
  {
    title: "escritorio",
    items: ["Kubuntu / KDE Plasma", "kitty + Starship", "Hyprland (en VM)"],
  },
];

// ============================================
// RENDER
// ============================================

function renderFetch() {
  const dl = document.getElementById("fetch-lines");
  FETCH_INFO.forEach(([key, value]) => {
    const dt = document.createElement("dt");
    dt.textContent = key;
    const dd = document.createElement("dd");
    dd.textContent = value;
    dl.append(dt, dd);
  });
}

function renderProjects() {
  const grid = document.getElementById("windows-grid");
  PROJECTS.forEach((p) => {
    const win = document.createElement("article");
    win.className = "window";
    win.innerHTML = `
      <div class="window__bar">
        <span class="term__dot term__dot--r"></span>
        <span class="term__dot term__dot--y"></span>
        <span class="term__dot term__dot--g"></span>
        <span class="window__name">${p.name}</span>
      </div>
      <div class="window__body">
        <h3 class="window__title">${p.title}</h3>
        <p class="window__desc">${p.desc}</p>
        <ul class="window__tags">
          ${p.tags.map((t) => `<li>${t}</li>`).join("")}
        </ul>
      </div>
    `;
    grid.appendChild(win);
  });
}

function renderStack() {
  const panels = document.getElementById("stack-panels");
  STACK.forEach((group) => {
    const panel = document.createElement("div");
    panel.className = "panel";
    panel.innerHTML = `
      <h3>${group.title}</h3>
      <ul>${group.items.map((i) => `<li>${i}</li>`).join("")}</ul>
    `;
    panels.appendChild(panel);
  });
}

// ============================================
// INIT
// ============================================

document.getElementById("year").textContent = new Date().getFullYear();

renderFetch();
renderProjects();
renderStack();
