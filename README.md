# Dashboard Ideal para Restaurantes NoSQL & Streamlit 🍽️

[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://mongodb.com)
[![Node.js](https://img.shields.io/badge/Node.js-14+-blue.svg)](https://nodejs.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://dash-restaurante.streamlit.app)


### Sistema de Avaliação de Restaurantes Online com MongoDB
- Este projeto demonstra a construção de uma plataforma de dados ponta-a-ponta, simulando um ambiente como o do iFood, para resolver o desafio central de restaurantes: **entender o comportamento do cliente para otimizar operações e aumentar a receita**. Utilizando uma stack moderna com MongoDB, Python e Streamlit, a solução permite que gestores de restaurantes respondam a perguntas críticas de negócio em tempo real.

## Principais conquistas
- **Visão 360º do Cliente**: Centralização de pedidos, avaliações e perfis de usuários em um banco de dados NoSQL, permitindo análises complexas de padrões de consumo.

- **Tomada de Decisão em Tempo Real**: Desenvolvimento de um dashboard interativo em Streamlit que traduz dados brutos em insights acionáveis, como identificação de pratos mais populares e horários de pico.

- **Arquitetura Escalável**: Criação de uma base de dados robusta com MongoDB, projetada para suportar milhões de pedidos e consultas geoespaciais de baixa latência, essenciais para um serviço de delivery.

## Problema de Negócio
No competitivo mercado de food service, pequenos e médios restaurantes enfrentam grandes desafios:
- **Falta de Visibilidade**: Dificuldade em entender quais pratos geram mais lucro, quais são os horários de maior movimento e qual o perfil do cliente mais fiel.
- **Operações Ineficientes**: Alocação de equipe e estoque baseada em intuição, e não em dados, gerando custos desnecessários.
- **Decisões Lentas**: A incapacidade de reagir rapidamente às tendências do mercado e ao feedback dos clientes.

O Food Journal foi projetado para ser a central de inteligência de negócio que resolve exatamente esses problemas. 

## 📈 Dashboard

Acesse o dashboard interativo desenvolvido em Streamlit:

🔗 **[Dashboard Food Journal](https://dash-restaurante.streamlit.app)**

O dashboard apresenta métricas de pedidos em tempo real:
- 📈 Identificar o Ticket Médio por Hora: Para criar promoções relâmpago em horários de baixo movimento.
- 📍 Visualizar um Mapa de Calor de Pedidos: Para otimizar a logística de entrega e avaliar a abertura de novas filiais.
- ⭐ Analisar a Correlação entre Avaliações e Pratos: Para destacar os pratos mais amados no cardápio e identificar aqueles que precisam de melhoria. 


<details>
<summary><strong>Clique para ver os Detalhes Técnicos, Arquitetura e Funcionalidades</strong></summary>
<br>

## 📋 Sobre o Projeto

O **Food Journal** é um sistema completo de avaliação de restaurantes online que permite aos usuários encontrar, avaliar e fazer pedidos em restaurantes. O projeto foi desenvolvido utilizando MongoDB como banco de dados NoSQL, aproveitando sua flexibilidade e escalabilidade para gerenciar dados complexos de forma eficiente.

### ✨ Principais Funcionalidades

- 👥 **Gestão de Usuários**: Cadastro, autenticação e perfis personalizados
- 🏪 **Catálogo de Restaurantes**: Cadastro completo com cardápios e geolocalização
- 🛒 **Sistema de Pedidos**: Criação, acompanhamento e histórico de pedidos
- ⭐ **Avaliações**: Sistema de notas e comentários com fotos
- 🔍 **Busca Avançada**: Filtros por localização, categoria, preço e preferências
- 📱 **Notificações**: Comunicação em tempo real entre clientes e restaurantes
- 📊 **Relatórios**: Dashboard com métricas de desempenho

## 🏗️ Arquitetura

### Modelo de Dados NoSQL

O sistema utiliza um modelo orientado a documentos com as seguintes coleções principais:

```
├── usuarios/          # Dados dos usuários
├── restaurantes/      # Informações dos estabelecimentos
├── cardapios/         # Cardápios dos restaurantes
├── pratos/           # Itens disponíveis
├── pedidos/          # Pedidos realizados
├── avaliacoes/       # Avaliações e comentários
├── notificacoes/     # Sistema de notificações
├── mensagens/        # Chat cliente-restaurantes
└── relatorios/       # Dados agregados
```

### Estratégias de Modelagem

- **Desnormalização Seletiva**: Dados frequentemente acessados juntos
- **Documentos Aninhados**: Relações 1:1 e 1:poucos
- **Arrays de Subdocumentos**: Listas de itens relacionados
- **Referências por ID**: Relações muitos-para-muitos
- **Índices Estratégicos**: Otimização de consultas críticas

</details>
<details>
<summary><strong>Clique para ver o Guia de Instalação e Configuração Local</strong></summary>
<br>

## 🚀 Instalação e Configuração

### Pré-requisitos

- Node.js 14+
- MongoDB 4.4+
- npm ou yarn

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/dashboard-restaurante-NoSQL.git
cd food-journal
```

2. **Instale as dependências**
```bash
npm install
```

3. **Configure o MongoDB**
```bash
# Inicie o MongoDB
mongod

# Crie o banco de dados
mongo
use dashboard-restaurante-NoSQL
```

4. **Popule o banco de dados**
```bash
node populate_db.js
```

### Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URI=mongodb://localhost:27017/dashboard-restaurante-NoSQL
PORT=3000
JWT_SECRET=seu_jwt_secret_aqui
```

## 📊 População de Dados

O projeto inclui um script `populate_db.js` que utiliza a biblioteca Faker.js para gerar dados realistas:

- **20.000 pedidos** simulando cenários reais
- Distribuição de horários de pico (almoço e jantar)
- Dados geográficos para testes de proximidade
- Integridade referencial entre todas as coleções

```bash
# Executar população de dados
node populate_db.js

# Configurar quantidade de dados (opcional)
# Edite as variáveis no início do arquivo populate_db.js
```


## 🔍 Principais Índices

### Usuários
```javascript
db.usuarios.createIndex({ email: 1 }, { unique: true });
db.usuarios.createIndex({ "endereco.cep": 1 });
db.usuarios.createIndex({ preferencias_alimentares: 1 });
```

### Restaurantes
```javascript
db.restaurantes.createIndex({ nome: "text", descricao: "text" });
db.restaurantes.createIndex({ categorias: 1 });
db.restaurantes.createIndex({ "endereco.coordenadas": "2dsphere" });
db.restaurantes.createIndex({ avaliacao_media: -1 });
```

### Pedidos
```javascript
db.pedidos.createIndex({ numero_pedido: 1 }, { unique: true });
db.pedidos.createIndex({ usuario_id: 1, data_hora_pedido: -1 });
db.pedidos.createIndex({ restaurante_id: 1, status_pedido: 1 });
```

## 🏃‍♂️ Como Usar

### Exemplos de Consultas

**Buscar restaurantes próximos:**
```javascript
db.restaurantes.find({
  "endereco.coordenadas": {
    $near: {
      $geometry: { type: "Point", coordinates: [-23.5505, -46.6333] },
      $maxDistance: 5000
    }
  }
});
```

**Pedidos de um usuário:**
```javascript
db.pedidos.find({ usuario_id: ObjectId("...") })
  .sort({ data_hora_pedido: -1 })
  .limit(10);
```

**Restaurantes por categoria:**
```javascript
db.restaurantes.find({ 
  categorias: "italiana",
  avaliacao_media: { $gte: 4.0 }
}).sort({ avaliacao_media: -1 });
```
</details>

## 👥 Equipe de Desenvolvimento

- **Felipe Teodoro**
- **Lucas Wall**  

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos issues do GitHub

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
