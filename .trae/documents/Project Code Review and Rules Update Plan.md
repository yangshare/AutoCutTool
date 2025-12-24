# Project Audit & Rule Enhancement Plan

Based on the review of the current codebase and project rules, I have identified areas for improvement in both the governance documentation and the code structure.

## 1. Code Review Findings
*   **Backend (`backend/`)**:
    *   **Strengths**: Good layered architecture (`api`, `domain`, `infra`). `server.py` has proper global exception handling and CORS setup.
    *   **Issues**:
        *   `infra/logger.py`: Uses a relative `logs` path, which might fail or create logs in unexpected places if the working directory changes.
        *   `pyproject.toml`: Dependencies are well-defined, but the list is long; ensure all are actually used.
*   **Frontend (`desktop/`)**:
    *   **Strengths**: Modern stack (Electron + Vite + React). Security best practices (`contextIsolation: true`) are followed.
    *   **Issues**:
        *   `electron/main.ts`: Contains business logic (`get-first-image` handler) mixed with window management code. This violates the Single Responsibility Principle.

## 2. Rules Review Findings
*   **Current State**: The rules (`startup.md`, `structure.md`) effectively cover *how* to run the project and where files are.
*   **Missing Elements**:
    *   **Code Style**: No explicit standards for linting or formatting (e.g., "Use Ruff for Python", "Use Prettier for TS").
    *   **Testing**: No guidelines on testing requirements.
    *   **Git Workflow**: No commit message conventions.

## 3. Implementation Plan

### Phase 1: Enhance Project Rules
Update `.trae/rules/dev_conventions.md` to include:
1.  **Code Style**:
    *   **Python**: Enforce PEP 8 using `ruff` (or `flake8`/`black`).
    *   **TypeScript**: Enforce `eslint` and `prettier`.
2.  **Testing Strategy**:
    *   Require unit tests for complex `domain` logic.
3.  **Git Conventions**:
    *   Suggest semantic commit messages (e.g., `feat:`, `fix:`).

### Phase 2: Refactor Codebase
1.  **Backend Logging**:
    *   Modify `backend/infra/logger.py` to use an absolute path for the `logs` directory (relative to the project root) to ensure reliability.
2.  **Frontend IPC Separation**:
    *   Extract the image processing logic (`get-first-image`) from `desktop/electron/main.ts` into a dedicated handler/controller file (e.g., `desktop/electron/handlers/imageHandler.ts`).

### Phase 3: Verification
1.  Verify the backend starts and logs correctly to the new path.
2.  Verify the desktop app builds and the image extraction feature still works after refactoring.
