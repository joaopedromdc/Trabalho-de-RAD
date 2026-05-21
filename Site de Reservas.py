import tkinter
import sqlite3
import hashlib
import re
from datetime import datetime

# ========== BANCO DE DADOS ==========
connection = sqlite3.connect("reservas.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        matricula INTEGER PRIMARY KEY,
        nome TEXT,
        curso TEXT,
        senha TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula_aluno INTEGER,
        data TEXT,
        hora TEXT,
        duracao INTEGER,
        quarto INTEGER
    )
""")

cursor.execute("SELECT * FROM alunos")
if not cursor.fetchall():

    alunos_exemplo = [
        (2021001, "João Silva", "Computação", hashlib.sha256(b"123").hexdigest()),
        (2021002, "Maria Santos", "Engenharia", hashlib.sha256(b"123").hexdigest()),
        (2021003, "Pedro Costa", "Matemática", hashlib.sha256(b"123").hexdigest())
    ]
    cursor.executemany("INSERT INTO alunos VALUES (?,?,?,?)", alunos_exemplo)
    connection.commit()

# ========== FUNÇÕES ==========
def verificar_aluno():
    matricula = entry_matricula.get()
    senha = entry_senha.get()
    
    if not matricula or not senha:
        label_mensagem.config(text="❌ Preencha todos os campos!", fg="red")
        return
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute("SELECT * FROM alunos WHERE matricula = ? AND senha = ?", 
                   (matricula, senha_hash))
    aluno = cursor.fetchone()
    
    if aluno:
        label_mensagem.config(text=f"✅ Bem-vindo {aluno[1]}!", fg="green")
        label_info.config(text=f"Aluno: {aluno[1]} | Curso: {aluno[2]}")
        entry_hora.config(state="normal")
        spin_duracao.config(state="normal")
        spin_quarto.config(state="normal")
        btn_reservar.config(state="normal")
        btn_ver_reservas.config(state="normal")
        btn_logout.config(state="normal")
        btn_reservar.matricula = matricula
    else:
        label_mensagem.config(text=" Matrícula ou senha inválida!", fg="red")

def validar_hora(hora):
    return re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", hora)

def fazer_reserva():
    matricula = btn_reservar.matricula
    hora = entry_hora.get()
    duracao = spin_duracao.get()
    quarto = spin_quarto.get()
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    if not hora:
        label_mensagem.config(text="❌ Digite a hora!", fg="red")
        return
    
    if not validar_hora(hora):
        label_mensagem.config(text="❌ Hora inválida! Use HH:MM", fg="red")
        return
 
    cursor.execute("""
        SELECT * FROM reservas 
        WHERE quarto = ? AND hora = ? AND data = ?
    """, (quarto, hora, data_atual))
    
    if cursor.fetchone():
        label_mensagem.config(text=f"❌ Quarto {quarto} já reservado neste horário!", fg="red")
        return
    
    cursor.execute("""
        INSERT INTO reservas (matricula_aluno, data, hora, duracao, quarto)
        VALUES (?, ?, ?, ?, ?)
    """, (matricula, data_atual, hora, duracao, quarto))
    connection.commit()
    
    valor = int(duracao) * 10
    label_mensagem.config(text=f"✅ Reservado! Quarto {quarto} - {duracao}h - R${valor}", fg="green")
    
    entry_hora.delete(0, tkinter.END)

def ver_reservas():
    matricula = btn_reservar.matricula
    
    cursor.execute("SELECT * FROM reservas WHERE matricula_aluno = ?", (matricula,))
    reservas = cursor.fetchall()
    
    if not reservas:
        label_mensagem.config(text="📭 Você não tem reservas", fg="blue")
        return
   
    janela = tkinter.Toplevel(root)
    janela.title("Minhas Reservas")
    janela.geometry("400x300")
    
    texto = "📋 SUAS RESERVAS:\n\n"
    for r in reservas:
        texto += f"📅 {r[2]} | 🕐 {r[3]}h | ⏱️ {r[4]}h | 🚪 Quarto {r[5]} | 💰 R${int(r[4])*10}\n"
    
    label = tkinter.Label(janela, text=texto, justify="left", font=("Arial", 10))
    label.pack(pady=20)
    
    btn_fechar = tkinter.Button(janela, text="Fechar", command=janela.destroy)
    btn_fechar.pack()

def logout():

    entry_matricula.delete(0, tkinter.END)
    entry_senha.delete(0, tkinter.END)
    entry_hora.delete(0, tkinter.END)
    entry_hora.config(state="disabled")
    spin_duracao.config(state="disabled")
    spin_quarto.config(state="disabled")
    btn_reservar.config(state="disabled")
    btn_ver_reservas.config(state="disabled")
    btn_logout.config(state="disabled")
    
    label_info.config(text="")
    label_mensagem.config(text="🔓 Faça login para continuar", fg="blue")

# ========== INTERFACE ==========
root = tkinter.Tk()
root.title("Sistema de Reserva de Quartos")
root.geometry("500x550")

titulo = tkinter.Label(root, text="🏠 RESERVA DE QUARTOS", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

frame_login = tkinter.LabelFrame(root, text="LOGIN DO ALUNO", padx=10, pady=10)
frame_login.pack(fill="x", padx=20, pady=10)

label_matricula = tkinter.Label(frame_login, text="Matrícula:")
label_matricula.grid(row=0, column=0, pady=5)
entry_matricula = tkinter.Entry(frame_login, width=30)
entry_matricula.grid(row=0, column=1, pady=5)

label_senha = tkinter.Label(frame_login, text="Senha:")
label_senha.grid(row=1, column=0, pady=5)
entry_senha = tkinter.Entry(frame_login, show="*", width=30)
entry_senha.grid(row=1, column=1, pady=5)

btn_login = tkinter.Button(frame_login, text="LOGIN", command=verificar_aluno, bg="green", fg="white")
btn_login.grid(row=2, column=0, columnspan=2, pady=10)

label_info = tkinter.Label(root, text="", font=("Arial", 10))
label_info.pack(pady=5)

frame_reserva = tkinter.LabelFrame(root, text="FAZER RESERVA", padx=10, pady=10)
frame_reserva.pack(fill="x", padx=20, pady=10)

label_hora = tkinter.Label(frame_reserva, text="Hora (HH:MM):")
label_hora.grid(row=0, column=0, pady=5)
entry_hora = tkinter.Entry(frame_reserva, width=20, state="disabled")
entry_hora.grid(row=0, column=1, pady=5)
label_exemplo_hora = tkinter.Label(frame_reserva, text="Ex: 14:30", fg="gray")
label_exemplo_hora.grid(row=0, column=2, pady=5)

label_duracao = tkinter.Label(frame_reserva, text="Duração (1-4h):")
label_duracao.grid(row=1, column=0, pady=5)
spin_duracao = tkinter.Spinbox(frame_reserva, from_=1, to=4, width=18, state="disabled")
spin_duracao.grid(row=1, column=1, pady=5)
label_exemplo_duracao = tkinter.Label(frame_reserva, text="Ex: 2 horas", fg="gray")
label_exemplo_duracao.grid(row=1, column=2, pady=5)

label_quarto = tkinter.Label(frame_reserva, text="Nº Quarto:")
label_quarto.grid(row=2, column=0, pady=5)
spin_quarto = tkinter.Spinbox(frame_reserva, from_=1, to=10, width=18, state="disabled")
spin_quarto.grid(row=2, column=1, pady=5)
label_exemplo_quarto = tkinter.Label(frame_reserva, text="Ex: 1 a 10", fg="gray")
label_exemplo_quarto.grid(row=2, column=2, pady=5)

label_valor = tkinter.Label(frame_reserva, text="💰 Valor: R$10,00 por hora", fg="blue")
label_valor.grid(row=3, column=0, columnspan=3, pady=10)

btn_reservar = tkinter.Button(frame_reserva, text="RESERVAR", command=fazer_reserva, 
                               bg="blue", fg="white", state="disabled")
btn_reservar.grid(row=4, column=0, columnspan=3, pady=5)

frame_botoes = tkinter.Frame(root)
frame_botoes.pack(pady=10)

btn_ver_reservas = tkinter.Button(frame_botoes, text="VER MINHAS RESERVAS", 
                                   command=ver_reservas, state="disabled")
btn_ver_reservas.pack(side="left", padx=5)

btn_logout = tkinter.Button(frame_botoes, text="LOGOUT", command=logout, 
                             bg="red", fg="white", state="disabled")
btn_logout.pack(side="left", padx=5)

btn_sair = tkinter.Button(frame_botoes, text="SAIR", command=root.destroy, bg="gray", fg="white")
btn_sair.pack(side="left", padx=5)

label_mensagem = tkinter.Label(root, text="🔐 Faça login para começar", font=("Arial", 9))
label_mensagem.pack(pady=20)

frame_exemplo = tkinter.LabelFrame(root, text="ALUNOS EXEMPLO", padx=10, pady=5)
frame_exemplo.pack(fill="x", padx=20, pady=10)

texto_exemplo = """
📚 Alunos cadastrados:
• Matrícula: 2021001 | Senha: 123 | João Silva - Computação
• Matrícula: 2021002 | Senha: 123 | Maria Santos - Engenharia  
• Matrícula: 2021003 | Senha: 123 | Pedro Costa - Matemática
"""

label_exemplo = tkinter.Label(frame_exemplo, text=texto_exemplo, justify="left", font=("Arial", 9), fg="gray")
label_exemplo.pack()

root.mainloop()

connection.close()
