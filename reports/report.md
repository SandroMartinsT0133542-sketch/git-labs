# Relatório de Projeto Web - Git & GitHub

**Aluno:** Sandro Ferreira Martins  
**Número:** 0133542  
**Email:** Sandro.Martins.T0133542@edu.atec.pt  
**Data:** 2026-05-04

## Objetivo

Demonstração prática e completa de conceitos de Git e GitHub através de um projeto web simples, incluindo:
- Inicialização e configuração de repositório Git local
- Commits incrementais com mensagens descritivas
- Análise de repositório (status, diff, log)
- Gestão de branches (criação, merge)
- Resolução de conflitos intencional
- Versionamento com tags

## 1. Inicialização do Repositório

### Processo
```bash
git init
git config user.name "Sandro Ferreira Martins"
git config user.email "Sandro.Martins.T0133542@edu.atec.pt"
```

**Evidência:** [reports/01-git-status-clean.txt](reports/01-git-status-clean.txt)

## 2. Commits Incrementais

### Commit 1: Documentação
```bash
git add README.md
git commit -m "docs: Add README with project description and instructions"
```
Hash: `bc7188c`

### Commit 2: Estrutura Web
```bash
git add index.html styles.css script.js
git commit -m "feat: Add web skeleton (HTML, CSS, JavaScript)"
```
Hash: `3800359`

**Estrutura criada:**
- `index.html` — Página HTML com identificação do aluno
- `styles.css` — Estilos CSS com gradiente e layout
- `script.js` — Script JavaScript que modifica o DOM

### Commit 3: Funcionalidade A
```bash
git checkout -b feature/alunoA
# Modificação de index.html
git add index.html
git commit -m "feat(alunoA): Add feature A implementation"
```
Hash: `5354d65`

### Commit 4: Funcionalidade B
```bash
git checkout -b feature/alunoB
# Modificação diferente de index.html
git add index.html
git commit -m "feat(alunoB): Add alternative feature B implementation"
```
Hash: `513bce6`

## 3. Análise e Histórico

### git status (Estado Inicial)
**Evidência:** [reports/01-git-status-clean.txt](reports/01-git-status-clean.txt)

### git log (Histórico Inicial)
**Evidência:** [reports/02-git-log-initial.txt](reports/02-git-log-initial.txt)

### git log (Pós-Merge)
**Evidência:** [reports/06-git-log-postmerge.txt](reports/06-git-log-postmerge.txt)

## 4. Branches e Merge

### Criação de Branches
1. `feature/alunoA` — Branch com implementação A
2. `feature/alunoB` — Branch com implementação B alternativa

### Merge com Conflito Intencional
```bash
git checkout feature/alunoA
git merge feature/alunoB --no-ff
```

**Resultado:** Conflito detectado na mesma linha do ficheiro `index.html`

**Evidência do conflito:**
- [reports/03-merge-conflict-log.txt](reports/03-merge-conflict-log.txt)
- [reports/04-git-status-conflict.txt](reports/04-git-status-conflict.txt)
- [reports/05-git-diff-conflict.txt](reports/05-git-diff-conflict.txt)

### Marcadores de Conflito
```html
<<<<<<< HEAD
    <p><strong>Branch A:</strong> Implementação de funcionalidade específica para Aluno A</p>
=======
    <p><strong>Branch B:</strong> Implementação alternativa de funcionalidade para Aluno B</p>
>>>>>>> feature/alunoB
```

### Resolução Manual
Resolvido combinando as duas funcionalidades:
```html
    <p><strong>Resolução:</strong> Funcionalidades de Aluno A e Aluno B integradas com sucesso!</p>
```

**Commit de resolução:**
```bash
git add index.html
git commit -m "fix: Resolve merge conflict - integrate features A and B"
```
Hash: `1cdf758`

## 5. Tags e Versionamento

### Tags Criadas

#### Tag Lightweight
```bash
git tag v1.0.0 -m "Version 1.0.0 - Initial release"
```

#### Tag Anotada
```bash
git tag -a v1.1.0 -m "Version 1.1.0 - After conflict resolution"
```

**Lista de tags:**
```
v1.0.0  Version 1.0.0 - Initial release
v1.1.0  Version 1.1.0 - After conflict resolution
```

**Evidência:** [reports/07-tags-list.txt](reports/07-tags-list.txt)

## 6. Estrutura do Projeto Final

```
git-labs/
├── README.md
├── index.html
├── styles.css
├── script.js
└── reports/
    ├── report.md (este ficheiro)
    ├── 01-git-status-clean.txt
    ├── 02-git-log-initial.txt
    ├── 03-merge-conflict-log.txt
    ├── 04-git-status-conflict.txt
    ├── 05-git-diff-conflict.txt
    ├── 06-git-log-postmerge.txt
    └── 07-tags-list.txt
```

## 7. Como Executar Localmente

```powershell
python -m http.server 8000
```

Abrir: `http://localhost:8000/index.html`

## 8. Conclusões

Este projeto demonstra corretamente:
- ✅ Inicialização de repositório Git local com configuração de utilizador
- ✅ Commits incrementais com mensagens claras e descritivas
- ✅ Uso consciente de `git status`, `git diff`, `git log`
- ✅ Criação de branches e merge com conflito intencional
- ✅ Resolução manual de conflito e respetivo commit
- ✅ Versionamento com tags (lightweight e anotada)
- ✅ Documentação completa com evidências

---

**Relatório gerado automaticamente em 2026-05-04**
