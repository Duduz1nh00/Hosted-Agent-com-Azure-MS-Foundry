# 🤖 Hosted Agent on Azure AI Foundry & Azure Container Apps

Este repositório contém a arquitetura, código e automação para a implantação de um **Hosted Agent** conteinerizado no **Azure Container Apps**, integrado nativamente ao **Azure AI Foundry Gateway**.

A solução utiliza **Python (Flask)** para processar as requisições e faz chamadas ao modelo `gpt-5-nano` via **Managed Identity** (autenticação *passwordless* com a role `Cognitive Services OpenAI User`), eliminando a necessidade de chaves de API codificadas.

---

## 📐 Arquitetura do Fluxo

```mermaid
sequenceDiagram
    autonumber
    actor Client as Cliente / App
    participant Gateway as Azure AI Foundry Gateway
    participant ACA as Azure Container Apps (agnttest)
    participant Model as Azure OpenAI (gpt-5-nano)

    Client->>Gateway: POST /protocols/openai/responses (com Bearer Token)
    Note over Gateway: Autenticação Entra ID & Roteamento via AgenticApplication
    Gateway->>ACA: Encaminha Requisição (mTLS / Internal Ingress)
    Note over ACA: Flask App processa a requisição
    ACA->>Model: Chamada via SDK usando System-Assigned Managed Identity
    Note over Model: Valida RBAC: Cognitive Services OpenAI User
    Model-->>ACA: Retorna resposta gerada pelo gpt-5-nano
    ACA-->>Gateway: Formata e envia resposta JSON (output_text)
    Gateway-->>Client: HTTP 200 OK


---
## 🏗️ Arquitetura da Solução

1. **Aplicação (Hosted Agent):** API Flask conteinerizada exposta via HTTPS na rota `/protocols/openai/responses`.
2. **Registro de Container:** Azure Container Registry (ACR) privado para armazenar a imagem Docker.
3. **Hospedagem:** Azure Container Apps executando em ambiente dedicado (`West US`).
4. **Segurança:** System-Assigned Managed Identity com acesso RBAC de menor privilégio no recurso do AI Foundry.
5. **Gateway de IA:** Roteamento via `AgenticApplication` do Azure AI Foundry REST API (`api-version=2026-05-15-preview`).

---
### 2. Pré-requisitos

Adicione esta seção logo antes de **Como Implantar** no seu `README.md`:

```markdown
## 📋 Pré-requisitos

Antes de iniciar a implantação, certifique-se de possuir:

* **Conta Azure Ativa**: Com permissões para criar e gerenciar recursos (`Contributor` / `Owner`).
* **Azure CLI (v2.60+)**: Instalada e autenticada (`az login`).
* **Docker Desktop**: Instalado e em execução para construção das imagens de container.
* **Recursos Provisionados no Azure**:
  * Assinatura Azure com acesso liberado aos serviços de IA.
  * Projeto e Recurso no **Azure AI Foundry** com o modelo `gpt-5-nano` implantado.
  * **Azure Container Registry (ACR)** configurado.
* **PowerShell 7+** ou **Bash**: Para execução dos scripts de automação.
## 🛠️ Tecnologias Utilizadas

* **Linguagens e Frameworks:** Python 3.10, Flask
* **Azure SDKs:** `azure-ai-projects`, `azure-identity`
* **Nuvem & Infraestrutura:** Azure Container Apps, Azure Container Registry (ACR), Azure AI Foundry
* **Segurança:** Azure RBAC, System-Assigned Managed Identity, Entra ID
* **Automação:** Azure CLI, PowerShell

---

## ⚡ Como Implantar

### 1. Conteinerização & Registro
```powershell
# Build e push da imagem para o ACR
docker build -t <SEU_ACR>.azurecr.io/agnttest:v1 .
az acr login --name <SEU_ACR>
docker push <SEU_ACR>.azurecr.io/agnttest:v1
