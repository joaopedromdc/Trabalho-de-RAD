# Atualizção 2.0 

## O que mudou?

### Antes (Versão 1)
- Todos os quartos custavam R$10,00 por hora
- Não tinha diferença entre quartos

### Depois (Versão 2)
- Quarto NORMAL: R$10,00 por hora
- Quarto PREMIUM: R$20,00 por hora
- O aluno pode escolher qual tipo quer na hora da reserva
- O valor total aparece automaticamente

---

## O que foi adicionado no código?

1. **Campo "Tipo do Quarto"** - Um menu com opções "Normal" e "Premium"

2. **Preço diferente** - Premium custa o dobro do Normal.

3. **Valor dinâmico** - Quando o aluno muda o tipo ou a duração, o preço atualiza na tela.

4. **Banco de dados** - Agora guarda também se a reserva foi Normal ou Premium.

5. **Listagem de reservas** - Mostra qual tipo de quarto foi reservado.

---

## Como testar as novidades?

1. Faça login com:
   - Matrícula: 2021001
   - Senha: 123

2. Preencha os dados:
   - Hora: 14:00
   - Duração: 2 horas
   - Tipo: PREMIUM (escolha no menu)
   - Quarto: 5

3. Veja o valor mudar sozinho na tela

4. Clique em RESERVAR

5. Clique em VER MINHAS RESERVAS - vai aparecer o tipo do quarto

---

## Problema que resolveu?

A empresa queria cobrar mais caro por quartos melhores (com cama maior, ar condicionado, etc). Agora o sistema permite isso.

---

## Arquivos modificados

- `reservas.db` - banco de dados (adicionado campo "tipo")
- Código Python - adicionadas as funções e interface para o novo recurso

---

## Observação

Ao rodar o código atualizado pela primeira vez, o sistema recria o banco de dados. As reservas antigas serão apagadas, mas os alunos continuam os mesmos.
