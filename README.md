# TCC - Qualidade de testes em ambiente integrado com DevOps

# DevOps
O que é DevOps?
*    DevOps é uma cultura que tem como objetivo integrar os times de desenvolvimento, operações de TI, engenharia da qualidade e segurança atuem um conjunto e com praticas destinadas a acelerar o tempo de desenvolvimento e entrega de software.



# Continuous Integration
O que é Continuous Integration?
*    Consiste na manutenção do código da aplicação atualizado afim de que os envolvidos no desenvolvimento do projeto possam ter acesso, auxiliando na detecção de Bugs, qualidade do software e desenvolvimento mais eficiente

# Continuous Delivery
O que é Continuous Delivery?
*   Conjunto de praticas automatizadas que tem como objetivo garantir que o código está apto para ser enviado para o ambiente de produção.

# Configurações Necessárias
Realize o download das plataformas necessárias:
*     - Cypress: Framework de automação de teste
        https://www.cypress.io/cloud
*     - Node.Js:
        https://nodejs.org/pt-br
*     - Cucumber: Framework para escrita de teste
        Plugin
*     - Visual Studio Code: Plataforma de desenvolvimento (IDE)
          https://code.visualstudio.com/

<details>
       <summary> Tipos de Testes </summary>

| Tipo de Teste|                                            Definição de teste                                            |
|:---:|:--------------------------------------------------------------------------------------------------------:|
| Unitários   |                         Testes funcionais das unidades ou componentes do código                          |
| Integração  |                      Verifica a integração entre diferentes componentes e sistemas                       |
| End to End  | Execução de testes em todo o sistema criado a fim de garantir que os componentes interagem adequadamente |
| Performance |                      Avalia a velocidade, escalabilidade e estabilidade do sistema                       |
| Segurança   |           Identifica as vulnerabilidades e garante a conformidade com os padrões de segurança            |

</details>

#### Resumo
O **Teste 03** foi reescrito para ser **independente** e robusto. Em vez de depender de um registro criado por outro teste ou de um ID fixo, o teste agora **cria o próprio registro** (com e‑mail único) e em seguida o edita. Também foram feitas melhorias na gestão do Playwright para evitar páginas fechadas entre testes.

#### O que foi feito
- **Isolamento do navegador**
  - O browser é aberto **uma vez por sessão**, mas cada teste cria um **novo context e uma nova page**. Isso evita o erro `TargetClosedError` causado por páginas “stale” ou fechadas por outros testes.
- **Independência do teste**
  - O teste 3 **cria via UI** um motorista com **e‑mail único** (timestamp) e só depois tenta editar esse mesmo registro. Assim o teste não depende de execução ou estado de outros testes.
- **Seletores mais confiáveis**
  - Em vez de usar `Editar.first` ou `id=1`, o teste localiza a **linha da tabela** que contém o e‑mail único e clica no botão **Editar** dentro dessa linha.
- **Espera explícita**
  - Foram adicionadas esperas explícitas (`wait_for_load_state`, `wait_for_selector`, `locator.wait_for`) para lidar com carregamento assíncrono da tabela e evitar condições de corrida.
- **Artefatos de depuração**
  - Em caso de falha, o teste salva **screenshot** e **HTML** em `tmp_test_artifacts/` para facilitar investigação.

#### Como o Teste 03 funciona agora
1. Gera um **e‑mail único**: `teste3_<timestamp>@example.com`.
2. Navega para `/motoristas/` e clica em **+ Novo Motorista**.
3. Preenche o formulário com o e‑mail único e salva.
4. Aguarda a listagem e localiza a **linha** que contém o e‑mail criado.
5. Clica em **Editar** nessa linha, altera campos e salva.
6. Valida que o registro editado aparece na listagem.

#### Comandos para executar os testes
- **Rodar com pytest (recomendado se estiver usando pytest-django)**
  ```bash
  pytest path/to/test_mecanica_pytest.py -q
  ```
  - Use os fixtures `live_server` e os fixtures Playwright fornecidos no arquivo de teste.
  - Não execute em paralelo (`pytest -n auto`) sem configurar bancos separados por worker.

- **Rodar com o test runner do Django** (se você manteve `LiveServerTestCase`)
  ```bash
  python manage.py test path.to.your.tests.test_mecanica
  ```

#### Observações e dicas de troubleshooting
- **Timeouts**: se o LiveServer estiver lento, aumente os timeouts (`wait_for_url`, `wait_for_selector`) para evitar falsos negativos.
- **Paralelização**: desative execução paralela enquanto usa o banco de teste padrão do Django ou configure bancos por worker.
- **Verificar artefatos**: em falhas, verifique `tmp_test_artifacts/*.png` e `*.html` para entender o estado da página no momento do erro.
- **Seletores**: se a tabela tiver estrutura diferente, ajuste o locator `tr` com `has_text=<email>` para corresponder ao HTML real. Cole um trecho do HTML se precisar que eu gere o seletor exato.
- **Banco de dados**: se preferir criar dados compartilhados uma vez por classe, use `setUpTestData` em `TestCase`, mas lembre-se de executar com `manage.py test` para evitar problemas de coleta do pytest.

#### Exemplo resumido para colar no README
> **Teste 03**: agora cria seu próprio registro via UI com e‑mail único, localiza a linha correspondente na tabela e edita esse registro. O browser é mantido por sessão, cada teste usa um novo context/page, e esperas explícitas garantem estabilidade contra carregamentos assíncronos. Em caso de falha, screenshots e HTML são salvos em `tmp_test_artifacts/`.

---

