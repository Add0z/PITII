Olá, estudante.  
A seguir, você dará continuidade ao desenvolvimento da sua solução através dos campos específicos para a resolução dos 3 desafios propostos, lembrando que eles se complementam.

**Nome:** André da Silveira Pereria  
**RGM:** 32235852

**Documentação:**  
**PIT I \- [https://github.com/Add0z/PITII/blob/main/docs/Relat%C3%B3rio%20de%20Entrega%20de%20Atividades%20Extensionistas.pdf](https://github.com/Add0z/PITII/blob/main/docs/Relat%C3%B3rio%20de%20Entrega%20de%20Atividades%20Extensionistas.pdf)**

**PIT II \-**   
***Link*** **do repositório:**   
[**https://github.com/Add0z/PITII**](https://github.com/Add0z/PITII)

**Codificação:**  
Na Tabela a seguir insira as informações referentes ao desenvolvimento do código do *front-end* e *back-end*.

| Linguagem do *Back-end* | Python3 |
| :---- | :---- |
| **Banco de Dados** | **SQLite** |
| **Hospedagem** | **Streamlit.app** |
| **Plataforma** | **web** |
| **Modo de Codificação** | ( x) Tradicional ( ) *Low-code* ( ) *No-code* |
| ***Link* do repositório no [GitHub](https://github.com/login) com os códigos abertos** | [https://github.com/Add0z/PITII](https://github.com/Add0z/PITII) |
| ***Link*** **da solução emfuncionamento** | [https://cupcakestore-pitii.streamlit.app/](https://cupcakestore-pitii.streamlit.app/) |
| ***Link*** **do vídeo narrado (no mínimo 5 min)**  |  |

**Testes da Solução**  
Escolha 5 colegas para testar sua aplicação e preencha a tabela a seguir com as informações obtidas:

| Nome:Aelcio Jozzia Putzel | Data do teste: 21/10/2025 |
| :---- | :---- |
| **O que testou e funcionou: Gestão de Itens: Adição/remoção de inventário.** |  |
| **O que testou e não funcionou – O que deve ser corrigido: Falha ao substituir um arquivo de imagem por outro com o mesmo nome na edição de um item.** |  |
| **Funcionalidade não testada (faltou ou não foi implementada):** |  |

| Nome:Laura Pereira  | Data do teste:05/11/2025  |
| :---- | :---- |
| **O que testou e funcionou: Configurações do Sistema: Atualização de dados cadastrais (endereço, formas de pagamento, etc.).** |  |
| **O que testou e não funcionou – O que deve ser corrigido: Ao clicar no logotipo da aplicação no painel de controle, a página atual é recarregada em vez de redirecionar para o *Dashboard* principal.** |  |
| **Funcionalidade não testada (faltou ou não foi implementada):** |  |

| Nome:Ricardo Costa | Data do teste: |
| :---- | :---- |
| **O que testou e funcionou: Acesso e Segurança: Criação de conta, login no sistema e atualização de dados pessoais.** |  |
| **O que testou e não funcionou – O que deve ser corrigido: Contas que foram desativadas/bloqueadas ainda conseguem fazer login.** |  |
| **Funcionalidade não testada (faltou ou não foi implementada):** |  |

| Nome:Mariana Santos | Data do teste:05/11/2025 |
| :---- | :---- |
| **O que testou e funcionou: Fluxo de Compra: Navegação na vitrine, adição ao carrinho e conclusão da transação (incluindo pagamentos por PIX e opções de retirada).** |  |
| **O que testou e não funcionou – O que deve ser corrigido: Erro ao tentar cancelar um pedido recém-finalizado com pagamento via PIX, exibindo a mensagem: "Erro ao remover item: registro indisponível."** |  |
| **Funcionalidade não testada (faltou ou não foi implementada):  opções de retirada** |  |

| Nome:Felipe Rocha  | Data do teste:05/11/2025 |
| :---- | :---- |
| **O que testou e funcionou: Interface de Usuário: Visualização de produtos, uso do carrinho de compras.** |  |
| **O que testou e não funcionou – O que deve ser corrigido: A validação do campo de quantidade no carrinho não impede a inserção de caracteres não numéricos.** |  |
| **Funcionalidade não testada (faltou ou não foi implementada):** |  |

**Laudo de Qualidade**

**Erros e Correções Identificados**

A seguir, estão detalhados os erros encontrados durante os testes e as correções propostas para garantir a estabilidade e a usabilidade do sistema:

| Testador | Funcionalidade Afetada | Descrição do Erro | Correção Proposta |
| ----- | ----- | ----- | ----- |
| **Aelcio Jozzia Putzel** | Gestão de Itens | Falha ao substituir um arquivo de imagem por outro com o mesmo nome na edição de um item. | Implementar uma rotina de *upload* que force a substituição do arquivo físico e/ou atualize o caminho da imagem no banco de dados, mesmo que o nome do arquivo permaneça o mesmo (ou utilizar um nome de arquivo único, como um *hash* ou *timestamp*, para evitar conflitos). |
| **Laura Pereira** | Interface/Navegação | Ao clicar no logotipo da aplicação no painel de controle, a página atual é recarregada em vez de redirecionar para o *Dashboard* principal. | Configurar o *link* do logotipo da aplicação para sempre redirecionar para a URL do *Dashboard* principal, independentemente da página atual. |
| **Ricardo Costa** | Acesso e Segurança | Contas que foram desativadas/bloqueadas ainda conseguem fazer login. | Implementar uma verificação de *status* da conta (ativo/bloqueado/desativado) no processo de autenticação (*login*). O acesso deve ser negado caso o *status* da conta não seja 'ativo'. |
| **Mariana Santos** | Fluxo de Compra (Cancelamento) | Erro ao tentar cancelar um pedido recém-finalizado com pagamento via PIX, exibindo a mensagem: "Erro ao remover item: registro indisponível." | Investigar a lógica de cancelamento de pedidos com pagamento PIX. O erro "registro indisponível" sugere que o pedido ou itens associados não estão sendo localizados corretamente para exclusão/atualização de *status* ou que há uma restrição de tempo/status para cancelamento que não está sendo verificada corretamente. |
| **Felipe Rocha** | Interface de Usuário (Carrinho) | A validação do campo de quantidade no carrinho não impede a inserção de caracteres não numéricos. | Implementar validação no *front-end* e *back-end* para garantir que o campo de quantidade aceite apenas caracteres numéricos inteiros e positivos. |

**Funcionalidades Não Testadas / Não Implementadas**

A funcionalidade de **opções de retirada** foi identificada por Mariana Santos como não testada ou não implementada no escopo dos testes realizados, o que exige atenção para o desenvolvimento ou inclusão em testes futuros.

**Vídeo da Solução atualizada**  
Após levantar os *feedbacks* e executar as correções necessárias e pertinentes, grave um vídeo de até 5 minutos apresentando as modificações realizadas no sistema.

| *Link* para o vídeo  | readme: [https://github.com/Add0z/PITII?tab=readme-ov-file](https://github.com/Add0z/PITII?tab=readme-ov-file) link: [https://github.com/Add0z/PITII/blob/main/docs/PITII-cupcakeShop-2x.mp4](https://github.com/Add0z/PITII/blob/main/docs/PITII-cupcakeShop-2x.mp4)  |
| :---- | :---- |

