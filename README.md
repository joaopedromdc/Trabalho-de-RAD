# Sistema de Reserva de Quartos - README

## 1. Contexto do Problema

Em faculdades públicas, um problema comum é o **tempo ocioso entre as aulas**. Alunos enfrentam intervalos de 1 a 4 horas sem um local adequado para descansar, estudar ou aguardar a próxima aula.

Uma empresa identificou essa necessidade e iniciou um negócio de aluguel de quartos por curtos períodos (1 a 4 horas), oferecendo espaços para descanso e estudo.

## 2. Objetivo do Trabalho

Desenvolver um aplicativo (simulado em Python) que permita aos alunos:
- Realizar reservas de quartos
- Informar o horário desejado para a reserva
- Informar o tempo esperado de uso (1 a 4 horas)
- Verificar se o usuário é um aluno matriculado

## 3. Motivação do Código

Este código foi desenvolvido com base no enunciado fornecido, pois:

| Necessidade do enunciado | Solução implementada no código |
|--------------------------|--------------------------------|
| Perguntar a hora da reserva | Input para horário no formato HH:MM |
| Perguntar o tempo esperado | Input validado entre 1 e 4 horas |
| Verificar se é aluno matriculado | Sistema de validação de matrícula |
| Reservar quartos | Estrutura de dados para controle de disponibilidade |


## 4. Adições pos-deploy

Foi adicionado classificação "premium" e "normal" aos quartos


