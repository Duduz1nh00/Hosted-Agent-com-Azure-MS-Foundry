# 🤖 Hosted Agent on Azure AI Foundry & Azure Container Apps

Este repositório contém a arquitetura, código e automação para a implantação de um **Hosted Agent** conteinerizado no **Azure Container Apps**, integrado nativamente ao **Azure AI Foundry Gateway**.

A solução utiliza **Python (Flask)** para processar as requisições e faz chamadas ao modelo `gpt-5-nano` via **Managed Identity** (autenticação *passwordless* com a role `Cognitive Services OpenAI User`), eliminando a necessidade de chaves de API codificadas.

---

## 🏗️ Arquitetura da Solução

1. **Aplicação (Hosted Agent):** API Flask conteinerizada exposta via HTTPS na rota `/protocols/openai/responses`.
2. **Registro de Container:** Azure Container Registry (ACR) privado para armazenar a imagem Docker.
3. **Hospedagem:** Azure Container Apps executando em ambiente dedicado (`West US`).
4. **Segurança:** System-Assigned Managed Identity com acesso RBAC de menor privilégio no recurso do AI Foundry.
5. **Gateway de IA:** Roteamento via `AgenticApplication` do Azure AI Foundry REST API (`api-version=2026-05-15-preview`).

---

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
