# 🍞 SaveByte

**Combatendo o desperdício de alimentos, um resgate por vez.**

SaveByte é uma plataforma que conecta estabelecimentos comerciais (padarias, restaurantes, mercados) que possuem excedentes de produção a consumidores finais dispostos a resgatar "cestas surpresa" por preços reduzidos — reduzindo o desperdício de alimentos e gerando economia para todos os envolvidos.

---

## 📋 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Problema e solução](#-problema-e-solução)
- [Usuários do sistema](#-usuários-do-sistema)
- [Funcionalidades principais](#-funcionalidades-principais)
- [Regras de negócio](#-regras-de-negócio)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Como executar o projeto](#-como-executar-o-projeto)
- [Limitações da versão atual](#-limitações-da-versão-atual)
- [Equipe](#-equipe)
- [Licença](#-licença)

---

## 🎯 Sobre o projeto

Atualmente, toneladas de alimentos próprios para consumo são descartadas diariamente por estabelecimentos comerciais devido à proximidade do vencimento ou ao encerramento do horário de funcionamento — gerando prejuízo financeiro e impacto ambiental. Do outro lado, consumidores buscam opções de alimentação mais acessíveis e sustentáveis.

O **SaveByte** atua nessa oportunidade de negócio conectando esses dois lados através de **ofertas relâmpago**: o estabelecimento publica o excedente do dia por um preço reduzido e dentro de uma janela de tempo curta, e o consumidor reserva, retira presencialmente e valida com um token único.

### 💚 Benefícios

- Redução direta do desperdício de alimentos e do impacto ambiental;
- Monetização de excedentes operacionais para os estabelecimentos parceiros;
- Acesso a alimentos de qualidade a preços reduzidos para a comunidade local;
- Estímulo ao comércio de bairro através do fluxo presencial gerado pelas retiradas;
- Gamificação: o consumidor acompanha quanta comida "salvou" e quanto dinheiro economizou.

## 🧩 Problema e solução

| Problema | Solução do SaveByte |
|---|---|
| Descarte precoce de alimentos próprios para consumo | Publicação de ofertas relâmpago com janela de tempo reduzida |
| Prejuízo financeiro do comerciante com excedentes | Monetização do excedente diário via venda a preço reduzido |
| Falta de acesso a alimentação acessível | Cestas surpresa com desconto significativo |
| Ausência de engajamento com sustentabilidade | Dashboard de gamificação de impacto ecológico e financeiro |

## 👥 Usuários do sistema

**Consumidor Final**
Navega pelas ofertas da região, reserva cestas, realiza o resgate presencial informando o token gerado e mantém seus dados cadastrais atualizados.

**Estabelecimento Comercial**
Cadastra a loja, publica ofertas relâmpago, valida o token apresentado pelo consumidor no momento do resgate e gerencia o estoque diário de cestas disponíveis.

## ⚙️ Funcionalidades principais

- 🔐 **Autenticação e gestão de perfis** geolocalizados (Consumidor e Estabelecimento);
- ⚡ **Publicação de Ofertas Relâmpago** com janela de tempo reduzida e contagem regressiva;
- 🔍 **Busca de ofertas** por proximidade geográfica e preferências alimentares;
- 🎟️ **Reserva de cestas** com geração de token numérico único para validação no local;
- 🔔 **Notificações** de novas ofertas no raio de alcance do usuário;
- ⚠️ **Sistema automático de penalidades** (strikes) por não comparecimento;
- 📊 **Dashboard de gamificação** com comida salva e economia acumulada.

### Requisitos funcionais

| Módulo | RF | Descrição |
|---|---|---|
| Autenticação & Perfis | RF01 | CRUD e login de Consumidores e Estabelecimentos |
| Gestão de Ofertas | RF02 | Cadastro de Ofertas Relâmpago com janela de tempo |
| Gestão de Ofertas | RF03 | Contagem regressiva da oferta |
| Gestão de Ofertas | RF04 | Busca por proximidade geográfica |
| Gestão de Ofertas | RF08 | Filtros de preferências alimentares |
| Reserva & Validação | RF05 | Reserva de Cestas Surpresa |
| Reserva & Validação | RF06 | Geração de token numérico único |
| Reserva & Validação | RF07 | Validação do token pelo estabelecimento |
| Reserva & Validação | RF11 | Cancelamento antecipado de reserva |
| Regras & Impacto | RF09 | Notificações de ofertas no raio de alcance |
| Regras & Impacto | RF10 | Aplicação automática de penalidades (strikes) |
| Regras & Impacto | RF12 | Dashboard de gamificação (comida salva e economia) |

## 📐 Regras de negócio

- **RN01 – Janela de Retirada Restrita:** uma reserva só é válida dentro da janela de tempo da oferta relâmpago; caso não seja retirada a tempo, a oferta passa para o status "Expirada".
- **RN02 – Raio de Ação de Resgate:** um usuário só consegue resgatar ofertas próximas à sua localização atual.
- **RN03 – Estorno Relâmpago Automático:** se o estabelecimento cancelar uma oferta relâmpago, o sistema estorna automaticamente o cliente e o prioriza nas próximas notificações de novas ofertas.
- **RN04 – Regra Anti-Acúmulo:** um mesmo consumidor não pode ter mais de duas reservas ativas ou retiradas simultaneamente em um período de 24h.
- **RN05 – Penalidade de No-Show:** se um consumidor reserva e não retira o alimento (status "Expirada"), sua conta recebe um *strike*. Dois strikes em 30 dias bloqueiam a conta para novas reservas por uma semana.

## 🛠️ Tecnologias utilizadas

| Categoria | Tecnologia |
|---|---|
| Linguagem / Interface gráfica | Python |
| Banco de dados | MongoDB |
| Segurança de senhas | bcrypt |
| Sistemas operacionais suportados | Linux (Ubuntu 26.04) e Windows 11 |
| Boas práticas | Clean Code |

## 🚀 Como executar o projeto

> 🚧 **Em definição.** As instruções de instalação e execução ainda serão adicionadas conforme o desenvolvimento avançar.

### Pré-requisitos (previstos)

- Python 3.10+
- MongoDB instalado localmente ou uma instância no MongoDB Atlas
- pip

## 🚧 Limitações da versão atual

- O sistema **não processa pagamentos reais** — apenas simula o estorno e o contrato de reserva;
- **Não há serviço de entrega (delivery)** integrado; a retirada é sempre presencial;
- O sistema **não gerencia o estoque interno completo** dos estabelecimentos, apenas o controle de cestas reservadas/disponíveis;
- A precisão da **geolocalização** está limitada à inserção de coordenadas/endereço pelo usuário ou à simulação do ambiente de desenvolvimento.

## 👨‍💻 Equipe

| Nome | GitHub |
|---|---|
| Matheus Ribeiro | [@usuario](https://github.com/) |
| Gabriel Henrique | [@usuario](https://github.com/) |
| Augusto Roberto | [@usuario](https://github.com/) |

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Análise de Projetos de Sistemas.
