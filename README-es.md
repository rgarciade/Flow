# flow

[Read in English](README.md)

**Issue-Driven Development** (desarrollo dirigido por issues) para agentes de programación con IA.

Un pequeño conjunto de [Agent Skills](https://agentskills.io/specification) para planificar el trabajo como tareas de tu gestor y desarrollarlo por porciones verticales, una a una, con la persona al mando.

> [!IMPORTANT]
> `flow` es estrictamente un flujo **desde las tareas**. El desarrollo dirigido por especificaciones parte de una especificación; `flow` parte de una tarea de tu gestor de tareas (un issue). No se construye nada sin ella: cada rama, test, commit y pull request pertenece a un issue, y el issue sigue siendo la fuente de verdad de lo que se pidió y de cómo se construyó.

<p align="center">
  <img src="docs/diagrams/overview.svg" alt="Las tres skills de flow y los archivos que leen y escriben" width="900">
</p>

## Cuándo usarlo

`flow` no pretende ser un estándar para cualquier proyecto. Encaja cuando hay incertidumbre y las cosas aún no están claras:

- **Un proyecto personal** en el que no sabes exactamente qué quieres construir y lo vas descubriendo poco a poco.
- **Un proyecto de trabajo con mucha indefinición**, donde los requisitos llegan tarde o cambian a menudo.
- **Un proyecto antiguo con un flujo basado en tareas**, como trabajaban muchos equipos antes de las especificaciones: el trabajo llega como tareas en un gestor y el código crece tarea a tarea.

Cuando el alcance está claro y es estable desde el principio, puede servirte mejor un enfoque dirigido por especificaciones como OpenSpec o BMAD (ver [IDD frente a SDD](docs/idd-vs-sdd.md)).

## Por qué

Los flujos dirigidos por especificaciones lo planifican todo de antemano, construyen capa a capa y acaban en pull requests enormes que nadie revisa de verdad. El desarrollo dirigido por issues hace lo contrario (comparación completa, y cuándo conviene más SDD: [IDD frente a SDD](docs/idd-vs-sdd.md)):

- **Estás dentro del flujo de principio a fin.** No es un trabajo que se lanza y se recoge después. Trabajas con el agente: te enseña lo que ha encontrado en cada fase, te pregunta siempre que algo no está decidido y espera tu OK antes de seguir. Es programación en pareja, y tú llevas el rumbo. Para una tarea sencilla puedes decirle que trabaje de forma autónoma: entonces solo para por lo que de verdad te necesita.
- **Visible desde el primer minuto, no al llegar el PR.** En equipos con desarrollo dirigido por especificaciones nadie sabe en qué punto está un desarrollo hasta que llega el pull request. Aquí la rama está enlazada al issue desde el principio, cada commit aprobado se sube, el plan está en el issue y su estado avanza (con tu OK) de en curso a en revisión.
- **Cualquier gestor de tareas.** GitHub Issues, GitLab, Jira, Linear, Azure Boards o archivos en el propio repo. `flow-setup` guarda cómo se hace cada operación en tu gestor, así que las tareas y sus registros quedan siempre igual; lo que el gestor no permita se resuelve con una alternativa acordada (por ejemplo, una carpeta del repo enlazada a la tarea).
- **El issue lo dirige todo.** Los requisitos viven en la descripción de la tarea, el plan de implementación en un registro y el resumen en otro. Cuando cambian los requisitos, se actualiza la descripción con un registro de qué cambió y por qué.
- **El detalle, justo a tiempo.** Una especificación intenta definirlo todo de antemano, y buena parte está obsoleta cuando alguien la construye. Un issue da la visión general, los pocos resultados que definen "terminado" y las pistas de una primera investigación (librerías, conectores, riesgos). Los criterios detallados, el diseño y los tests se deciden en la fase de plan, sobre el código tal como está cuando empieza la tarea. Es como se trabajaba antes de las especificaciones: sin suponer demasiado pronto, pero sin tickets vacíos.
- **La arquitectura se escribe mientras se construye.** Con tareas pequeñas se puede perder la visión global, así que `flow` la mantiene explícita: los issues padre llevan notas de arquitectura, cada plan señala sus decisiones de arquitectura, esas decisiones se convierten en ADR antes del PR, las revisiones contrastan el código con los ADR existentes y cada funcionalidad completa pasa una revisión de arquitectura antes de llegar a la rama base.
- **La documentación es parte de "terminado".** Cada plan lista los documentos del proyecto que afecta la tarea, se actualizan junto con la implementación y la revisión señala los que se hayan quedado desactualizados. La justa y necesaria: solo lo que el código no cuenta fácilmente. El issue guarda qué se pidió, los ADR el porqué y la documentación cómo funciona ahora.
- **Planificar poco, y cuando quieras.** Las tareas viven en tu gestor de tareas. Se crean en una sesión de planificación o justo antes de empezar una.
- **Una tarea, una porción vertical.** Cada tarea funciona de principio a fin cuando se termina y cabe en una sesión de trabajo. ¿Es demasiado grande? Se divide en tareas hijas.
- **Primero los tests, aprobados por ti.** La IA escribe los tests, tú los apruebas y a partir de ese momento quedan congelados: la implementación tiene que hacerlos pasar sin tocarlos. Si uno resulta estar mal, solo cambia con tu OK y en su propio commit.
- **La IA escribe y tú decides.** Nunca hace commits ni merges por su cuenta. Te da el comando y tú lo ejecutas, o le dices que lo haga.
- **Contexto pequeño, ayudantes especializados.** Un orquestador habla contigo y delega la investigación, la planificación, los tests, la implementación y la revisión en subagentes que comparten los detalles mediante notas (en Engram o, si no está disponible, en archivos).

## Las skills

- **[`flow-setup`](skills/flow-setup/SKILL.md)** · _Una vez por repo_  
  Pregunta qué gestor de tareas usas y escribe `docs/agents/` (cómo se hace cada operación con las tareas, documentación de dominio, configuración del flujo) para que las otras skills sepan cómo funciona ese repo.
- **[`flow-plan`](skills/flow-plan/SKILL.md)** · _Sesiones de planificación_  
  Convierte ideas en tareas de tu gestor: tareas sueltas, o una tarea padre con hijas y sus bloqueos. Sin código.
- **[`flow-work`](skills/flow-work/SKILL.md)** · _Desarrollar una tarea_  
  Lleva una tarea de la rama al PR: investigar → planificar → tests (con tu OK) → implementar + documentar → revisar → ADR → PR.

`flow-plan` y `flow-work` comprueban primero si existe `docs/agents/workflow.md` y, si falta, se ofrecen a ejecutar `flow-setup`.

## Cómo avanza una tarea

<p align="center">
  <a href="docs/flows.md"><img src="docs/diagrams/flow-work-phases.svg" alt="Fases de flow-work, con los puntos en los que decides tú y los commits" width="900"></a>
</p>

Todas las fases, ramas y subagentes, paso a paso (en inglés): **[docs/flows.md](docs/flows.md)**. Dónde viven los requisitos, el plan, los ADR y la documentación del proyecto, y cuándo se escribe cada uno: **[Where knowledge lives](docs/flows.md#where-knowledge-lives)**.

## Inicio rápido

```sh
# 1. Instala las skills (ver docs/setup.md)
./install.sh --project ~/code/mi-app      # en un repo, para cualquier entorno (copias versionadas)
./install.sh --user                       # o para tu usuario: OpenCode, Codex, Cursor, Gemini CLI
./install.sh --claude ~/.claude-personal  # o en un perfil de Claude Code

# 2. En el proyecto, abre tu agente y ejecuta:
/flow-setup          # una vez por repo
/flow-plan           # crear tareas
/flow-work #42       # desarrollar una
```

Funciona con cualquier entorno compatible con Agent Skills: Claude Code, OpenCode, Codex CLI, Cursor y Gemini CLI. Se desarrolla y se prueba en Claude Code; [setup.md](docs/setup.md) explica las diferencias.

**Dónde vive cada cosa.** Las skills se instalan una vez por usuario, o se copian en un repo cuando ese repo debe llevarlas consigo. Las reglas propias de cada repo viven en su `docs/agents/`, que escribe `flow-setup`: cómo funciona su gestor de tareas (`tracker.md`) y sus ramas, idiomas, modelos y comandos (`workflow.md`). Tu archivo de instrucciones generales (`CLAUDE.md`, `AGENTS.md`…) sigue siendo tuyo: `flow-setup` solo añade un bloque corto `## Agent skills` que apunta a `docs/agents/`.

## Documentación

La documentación detallada está en inglés:

- [IDD frente a SDD](docs/idd-vs-sdd.md): cómo se compara este flujo con el desarrollo dirigido por especificaciones y cuándo usar cada uno.
- [Instalación](docs/setup.md): requisitos, instalación y configuración de un repo.
- [Guía de uso](docs/usage.md): recetas para el día a día.
- [Flujos](docs/flows.md): cómo encajan las fases, las ramas y los subagentes.

## Créditos

- El método de trabajo se inspira en una charla que propone sustituir el desarrollo dirigido por especificaciones por backlog, historias de usuario, porciones verticales y programación en pareja con la IA.
- Algunas skills incluidas y referencias se adaptan de [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
