# Registro individual — AV1.1

**Estudante:** Pedro — **Data:** 16/10/2026
**Origem:** tarefas T1–T3 fictícias do enunciado. **Modalidade:** T1-A = *resposta simulada* (`apoio/respostas-simuladas/b1-cpf-completar.md`, texto do professor, não é saída real de modelo) **executada por mim numa cópia de trabalho**; T1-B e T2 = execução própria com agente.
**Critério de aceite (definido antes):** T1 — `v08` e `v09` passam, `v01–v07` e `v11` continuam passando, suíte existente (26) verde. T2 — `v10` passa (422 + campos `cpf`, `email`, `nome`) sem regredir as demais. Linha de base: 8/11 ok, falham `v08` (201≠422), `v09` (201≠422), `v10` (400≠422).

| Tarefa | Modo | 1ª versão | Pronto e verificado | Idas e vindas | % à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: completar no editor (simulada) | 2 min (simulado) | **não chegou a "pronto"** | 0 | ~40% (ligar `cpf_valido` ao cadastro e ao 422 foi à mão) | Não trata dígitos iguais: `111.111.111-11` e `00000000000` passam no algoritmo de DV → `v09` falha (201≠422). Só gera a função; não toca o status nem o formato `{"erros": [...]}` | Rodei a sugestão contra os 7 CPFs de `cpfs.json` e `--codigo` na cópia: v08 ok, **v09 FAIL**; `--existentes`: `test_cadastro_valido` FAIL (422≠201, sem cpf) |
| T1 | B: agente (Claude, Cowork) com escopo declarado: só `cadastro.py` + teste afetado | ~1 min | [preencher: tempo até eu revisar o diff] | 1 (pedido com escopo + R3) | 0% no código; revisão do diff | Nenhum erro funcional nesta execução. Risco que eu revisei: alterou `test_cadastro.py` (necessário — ver abaixo); não tocou `handlers.py` nem `testes/` | 11/11 + 26/26; checagem extra: válidos→True, DV errado→False, dígitos iguais→False, `"…-2a"`→False |
| T2 | Agente (mesma sessão de T1-B) | junto com T1-B | idem | 0 adicionais | 0% | — (fez T1 e T2 juntos; aceitei porque `v08` já exige o formato `erros` de R3.4) | `v10` ok; `cadastrar_cliente({})` devolve 422 com 3 erros |

**Evidência (comando e saída):** `python -B testes/test_miniloja.py --codigo caso` → `test_v08 ... ok`, `test_v09 ... ok`, `test_v10 ... ok`, `Ran 11 tests ... OK` (exit 0). `--existentes` → `Ran 26 tests ... OK`. Modo A na cópia: `test_v09 ... FAIL — AssertionError: 201 != 422`, `FAILED (failures=2)`.
**Teste existente alterado:** `caso/testes_existentes/test_cadastro.py` — R3.4 muda 400→422 com lista de erros e R3.1 torna `cpf` obrigatório; o caso válido passou a enviar CPF válido. `testes/` e `regras.md` não foram alterados.

**Por que cada modo:** A (completar) é bom para função pequena e local com oráculo claro, mas não enxerga o contrato inteiro (R3.2 tem duas condições). B (agente) faz sentido porque a mudança cruza código + teste existente e há oráculo executável (11 verificações) — desde que com escopo declarado, para evitar o que a simulação `b1-cpf-agente.md` mostra (mexeu em `handlers.py` sem pedido e declarou "todos os testes passam" sem cobrir dígitos iguais).

**T3 (hipotética, sem executar):** raio de impacto **alto** (produção, clientes reais, horário sem equipe); oráculo **fraco** (métricas mostram o sintoma, não confirmam a causa); reversibilidade **baixa** para comandos de escrita (restart, kill, mudança de config). **Modo:** agente/chat em **modo leitura** para diagnóstico. **Permissões:** leitura de métricas, logs e consultas de diagnóstico (`top`, `EXPLAIN`, listar conexões); **sem** escrita, restart, deploy ou acesso a dados de clientes. Ações corretivas: propostas pelo agente, executadas por humano com runbook e rollback.

**Alternativa e limite:** a alternativa a B em T1 seria A + teste manual dos casos de `cpfs.json`; custa mais tempo à mão, mas o escopo fica 100% sob meu controle. **Limite:** uma execução de cada modo, com uma resposta simulada no modo A — não prova nada sobre as ferramentas; só calibra meu julgamento. **Condição para mudar:** se não houvesse oráculo executável (sem `v08–v10`), eu não usaria agente para T1/T2; e se o agente tocasse arquivos fora do escopo, voltaria a A.

**Procedência/IA:** Claude (Cowork; modelo configurado `claude-opus-5-5`). Delegado: rodar a linha de base, executar a sugestão simulada do modo A, implementar T1+T2 em `cadastro.py`, ajustar o teste existente e rascunhar este registro. Minha verificação/intervenção: [preencher — ex.: revisei o diff, rodei os dois comandos na minha máquina]. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] dois modos em T1; [x] evidência localizada; [x] T3 decidida; [x] alternativa e limite; [x] até uma página.
