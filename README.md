# Dashboard Ideal para Restaurantes NoSQL & Streamlit 🍽️

Sistema de Avaliação de Restaurantes Online com MongoDB

[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://mongodb.com)
[![Node.js](https://img.shields.io/badge/Node.js-14+-blue.svg)](https://nodejs.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://dash-restaurante.streamlit.app)

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
├── mensagens/        # Chat cliente-restaurante
└── relatorios/       # Dados agregados
```

### Estratégias de Modelagem

- **Desnormalização Seletiva**: Dados frequentemente acessados juntos
- **Documentos Aninhados**: Relações 1:1 e 1:poucos
- **Arrays de Subdocumentos**: Listas de itens relacionados
- **Referências por ID**: Relações muitos-para-muitos
- **Índices Estratégicos**: Otimização de consultas críticas

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

## 📈 Dashboard

Acesse o dashboard interativo desenvolvido em Streamlit:

🔗 **[Dashboard Food Journal](https://dash-restaurante.streamlit.app)**

O dashboard apresenta:
- Métricas de pedidos em tempo real
- Análise de performance por restaurante
- Distribuição geográfica
- Tendências de avaliações
- Relatórios de faturamento

## 📋 Requisitos do Sistema

### Funcionais
- ✅ Cadastro e autenticação de usuários
- ✅ Gerenciamento de restaurantes e cardápios
- ✅ Sistema completo de pedidos
- ✅ Avaliações e comentários
- ✅ Busca geoespacial
- ✅ Notificações em tempo real
- ✅ Relatórios gerenciais

### Não-Funcionais
- ✅ Escalabilidade para milhões de usuários
- ✅ Alta disponibilidade (99.9% uptime)
- ✅ Baixa latência (<200ms)
- ✅ Conformidade com LGPD
- ✅ Suporte a consultas geoespaciais
- ✅ Resistência a picos de tráfego

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

## 👥 Equipe de Desenvolvimento

- **Felipe Teodoro**
- - **Lucas Wall**  
- **João Vitor**
- **Mateo Wall**

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
