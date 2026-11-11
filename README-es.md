# flow

[Read in English](README.md)

**Issue-Driven Development** (desarrollo dirigido por issues) para agentes de programación con IA.

Un pequeño conjunto de [Agent Skills](https://agentskills.io/specification) para planificar el trabajo como tareas de tu gestor y desarrollarlo por porciones verticales, una a una, con la persona al mando.

> [!NOTE]
> **Cuándo usarlo.** `flow` no pretende ser un estándar para cualquier proyecto. Encaja cuando hay incertidumbre y las cosas aún no están claras:
>
> - **Un proyecto personal** en el que no sabes exactamente qué quieres construir y lo vas descubriendo poco a poco.
> - **Un proyecto de trabajo con mucha indefinición**, donde los requisitos llegan tarde o cambian a menudo.
> - **Un proyecto antiguo con un flujo basado en tareas**: el trabajo llega como tareas en un gestor y el código crece tarea a tarea.
>
> Cuando el alcance está claro y es estable desde el principio, puede servirte mejor un enfoque dirigido por especificaciones como OpenSpec o BMAD (ver [IDD frente a SDD](docs/idd-vs-sdd.md)).

> [!IMPORTANT]
> `flow` es estrictamente un flujo **desde las tareas**. El desarrollo dirigido por especificaciones parte de una especificación; `flow` parte de una tarea de tu gestor de tareas (un issue). No se construye nada sin ella: cada rama, test, commit y pull request pertenece a un issue, y el issue sigue siendo la fuente de verdad de lo que se pidió y de cómo se construyó.

<p align="center">
  <img src="docs/diagrams/overview.svg" alt="Las tres skills de flow y los archivos que leen y escriben" width="900">
</p>

## Las skills

- **[`flow-setup`](skills/flow-setup/SKILL.md)** · _Una vez por repo_  
  Pregunta qué gestor de tareas usas y escribe `docs/agents/` (cómo se hace cada operación con las tareas, documentación de dominio, configuración del flujo) para que las otras skills sepan cómo funciona ese repo.
- **[`flow-backlog`](skills/flow-backlog/SKILL.md)** · _Sesiones de backlog_  
  Convierte ideas en tareas de tu gestor: tareas sueltas, o una tarea padre con hijas y sus bloqueos. Sin código.
- **[`flow-work`](skills/flow-work/SKILL.md)** · _Desarrollar una tarea_  
  Lleva una tarea de la rama al PR: investigar → planificar → tests (con tu OK) → implementar + documentar → revisar → ADR → PR.

`flow-backlog` y `flow-work` comprueban primero si existe `docs/agents/workflow.md` y, si falta, se ofrecen a ejecutar `flow-setup`.

## Cómo avanza una tarea

<p align="center">
  <a href="docs/flows.md"><img src="docs/diagrams/flow-work-phases.svg" alt="Fases de flow-work, con los puntos en los que decides tú y los commits" width="900"></a>
</p>

Todas las fases, ramas y subagentes, paso a paso (en inglés): **[docs/flows.md](docs/flows.md)**. Dónde viven los requisitos, el plan, los ADR y la documentación del proyecto, y cuándo se escribe cada uno: **[Where knowledge lives](docs/flows.md#where-knowledge-lives)**.

## Por qué

Los flujos dirigidos por especificaciones lo planifican todo de antemano y acaban en pull requests enormes que nadie revisa de verdad. `flow` avanza tarea a tarea ([IDD frente a SDD](docs/idd-vs-sdd.md)):

- **Estás dentro del flujo.** Te enseña cada fase, te pregunta cuando algo no está decidido y nunca hace commits ni merges por su cuenta.
- **El issue lo dirige todo.** Requisitos, plan y resumen viven en la tarea, en cualquier gestor: GitHub, GitLab, Jira, Linear o archivos.
- **El detalle, justo a tiempo.** El issue da la visión general; el plan decide criterios, diseño y tests sobre el código tal como está al empezar la tarea.
- **Una tarea, una porción vertical.** Cada una funciona de principio a fin y cabe en una sesión de trabajo. ¿Demasiado grande? Se divide en tareas hijas.
- **Primero los tests, y congelados.** La implementación tiene que hacerlos pasar sin tocarlos; cualquier cambio necesita tu OK.
- **Visible desde el primer minuto.** La rama está enlazada al issue, cada commit aprobado se sube y el estado avanza con tu OK.
- **Arquitectura y documentación sobre la marcha.** Las decisiones de arquitectura se convierten en ADR y la documentación afectada se actualiza antes del PR.

## Inicio rápido

```sh
# 1. Instala las skills (ver docs/setup.md)
./install.sh --project ~/code/mi-app      # en un repo, para cualquier entorno (copias versionadas)
./install.sh --user                       # o para tu usuario: OpenCode, Codex, Cursor, Gemini CLI
./install.sh --claude ~/.claude-personal  # o en un perfil de Claude Code

# 2. En el proyecto, abre tu agente y ejecuta:
/flow-setup          # una vez por repo
/flow-backlog        # crear tareas
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

## Licencia

[MIT](LICENSE). Las skills incluidas de terceros conservan su propia licencia en `vendor/mattpocock-skills/LICENSE`.
