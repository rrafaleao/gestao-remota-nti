import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

class AppCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Funcionários e Folha de Pagamento")
        self.conexao = mysql.connector.connect(
            host="6bvqh.h.filess.io",
            user="gestaoremota_inchmighty",
            password="b693e471d9316b51a132db1c63b9f9106fb47f82",
            database="gestaoremota_inchmighty",
            port="3307"
        )
        self.cursor = self.conexao.cursor()
        self.criar_interface()

    def criar_interface(self):
        # Abas para Funcionários e Folha de Pagamento
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        # Aba de Funcionários
        self.frame_funcionarios = Frame(self.notebook)
        self.notebook.add(self.frame_funcionarios, text="Funcionários")

        # Aba de Folha de Pagamento
        self.frame_folha = Frame(self.notebook)
        self.notebook.add(self.frame_folha, text="Folha de Pagamento")

        # Interface para Funcionários
        self.criar_interface_funcionarios()
        self.carregar_dados_funcionarios()

        # Interface para Folha de Pagamento
        self.criar_interface_folha()
        self.carregar_dados_folha()

    def criar_interface_funcionarios(self):
        # Frame do formulário de Funcionários
        self.frame_form_func = Frame(self.frame_funcionarios)
        self.frame_form_func.pack(pady=10)

        # Campos do formulário de Funcionários
        Label(self.frame_form_func, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = Entry(self.frame_form_func)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(self.frame_form_func, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
        self.cpf_entry = Entry(self.frame_form_func)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.frame_form_func, text="Cargo:").grid(row=2, column=0, padx=5, pady=5)
        self.cargo_entry = Entry(self.frame_form_func)
        self.cargo_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.frame_form_func, text="Departamento:").grid(row=3, column=0, padx=5, pady=5)
        self.departamento_entry = Entry(self.frame_form_func)
        self.departamento_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botões de Funcionários
        btn_frame_func = Frame(self.frame_funcionarios)
        btn_frame_func.pack(pady=10)

        btn_salvar_func = Button(btn_frame_func, text="Salvar", command=self.salvar_funcionario)
        btn_salvar_func.grid(row=0, column=0, padx=5)

        btn_editar_func = Button(btn_frame_func, text="Editar", command=self.editar_funcionario)
        btn_editar_func.grid(row=0, column=1, padx=5)

        btn_excluir_func = Button(btn_frame_func, text="Excluir", command=self.excluir_funcionario)
        btn_excluir_func.grid(row=0, column=2, padx=5)

        # Treeview de Funcionários
        self.tree_funcionarios = ttk.Treeview(self.frame_funcionarios, columns=('Nome', 'CPF', 'Cargo', 'Departamento'), show='headings')
        self.tree_funcionarios.heading('Nome', text='Nome')
        self.tree_funcionarios.heading('CPF', text='CPF')
        self.tree_funcionarios.heading('Cargo', text='Cargo')
        self.tree_funcionarios.heading('Departamento', text='Departamento')
        self.tree_funcionarios.pack(pady=10)

        # Vincular evento de seleção na Treeview de Funcionários
        self.tree_funcionarios.bind('<<TreeviewSelect>>', self.preencher_campos_funcionario)

    def criar_interface_folha(self):
        # Frame do formulário de Folha de Pagamento
        self.frame_form_folha = Frame(self.frame_folha)
        self.frame_form_folha.pack(pady=10)

        # Campos do formulário de Folha de Pagamento
        Label(self.frame_form_folha, text="Funcionário ID:").grid(row=0, column=0, padx=5, pady=5)
        self.funcionario_id_entry = Entry(self.frame_form_folha)
        self.funcionario_id_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(self.frame_form_folha, text="Mês/Ano (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.mes_ano_entry = Entry(self.frame_form_folha)
        self.mes_ano_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.frame_form_folha, text="Horas Trabalhadas:").grid(row=2, column=0, padx=5, pady=5)
        self.horas_trabalhadas_entry = Entry(self.frame_form_folha)
        self.horas_trabalhadas_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.frame_form_folha, text="Valor Pago:").grid(row=3, column=0, padx=5, pady=5)
        self.valor_pago_entry = Entry(self.frame_form_folha)
        self.valor_pago_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botões de Folha de Pagamento
        btn_frame_folha = Frame(self.frame_folha)
        btn_frame_folha.pack(pady=10)

        btn_salvar_folha = Button(btn_frame_folha, text="Salvar", command=self.salvar_folha)
        btn_salvar_folha.grid(row=0, column=0, padx=5)

        btn_editar_folha = Button(btn_frame_folha, text="Editar", command=self.editar_folha)
        btn_editar_folha.grid(row=0, column=1, padx=5)

        btn_excluir_folha = Button(btn_frame_folha, text="Excluir", command=self.excluir_folha)
        btn_excluir_folha.grid(row=0, column=2, padx=5)

        # Treeview de Folha de Pagamento
        self.tree_folha = ttk.Treeview(self.frame_folha, columns=('Funcionário ID', 'Mês/Ano', 'Horas Trabalhadas', 'Valor Pago'), show='headings')
        self.tree_folha.heading('Funcionário ID', text='Funcionário ID')
        self.tree_folha.heading('Mês/Ano', text='Mês/Ano')
        self.tree_folha.heading('Horas Trabalhadas', text='Horas Trabalhadas')
        self.tree_folha.heading('Valor Pago', text='Valor Pago')
        self.tree_folha.pack(pady=10)

        # Vincular evento de seleção na Treeview de Folha de Pagamento
        self.tree_folha.bind('<<TreeviewSelect>>', self.preencher_campos_folha)

    # Métodos para Funcionários
    def salvar_funcionario(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        cargo = self.cargo_entry.get()
        departamento = self.departamento_entry.get()

        if not nome or not cpf or not cargo or not departamento:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Funcionarios (nome, cpf, cargo, departamento) VALUES (%s, %s, %s, %s)",
                (nome, cpf, cargo, departamento)
            )
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Funcionário salvo!")
            self.limpar_campos_funcionario()
            self.carregar_dados_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def editar_funcionario(self):
        selected_item = self.tree_funcionarios.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um funcionário para editar!")
            return

        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        cargo = self.cargo_entry.get()
        departamento = self.departamento_entry.get()

        if not nome or not cpf or not cargo or not departamento:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            id_funcionario = self.tree_funcionarios.item(selected_item, 'text')
            self.cursor.execute(
                "UPDATE Funcionarios SET nome = %s, cpf = %s, cargo = %s, departamento = %s WHERE id = %s",
                (nome, cpf, cargo, departamento, id_funcionario)
            )
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Funcionário atualizado!")
            self.limpar_campos_funcionario()
            self.carregar_dados_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar: {e}")

    def excluir_funcionario(self):
        selected_item = self.tree_funcionarios.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
            return

        try:
            id_funcionario = self.tree_funcionarios.item(selected_item, 'text')
            self.cursor.execute("DELETE FROM Funcionarios WHERE id = %s", (id_funcionario,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Funcionário excluído!")
            self.limpar_campos_funcionario()
            self.carregar_dados_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir: {e}")

    def carregar_dados_funcionarios(self):
        self.tree_funcionarios.delete(*self.tree_funcionarios.get_children())
        self.cursor.execute("SELECT id, nome, cpf, cargo, departamento FROM Funcionarios")
        for row in self.cursor.fetchall():
            self.tree_funcionarios.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4]))

    def preencher_campos_funcionario(self, event):
        selected_item = self.tree_funcionarios.selection()
        if selected_item:
            values = self.tree_funcionarios.item(selected_item, 'values')
            self.nome_entry.delete(0, END)
            self.nome_entry.insert(0, values[0])
            self.cpf_entry.delete(0, END)
            self.cpf_entry.insert(0, values[1])
            self.cargo_entry.delete(0, END)
            self.cargo_entry.insert(0, values[2])
            self.departamento_entry.delete(0, END)
            self.departamento_entry.insert(0, values[3])

    def limpar_campos_funcionario(self):
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.cargo_entry.delete(0, END)
        self.departamento_entry.delete(0, END)

    # Métodos para Folha de Pagamento
    def salvar_folha(self):
        funcionario_id = self.funcionario_id_entry.get()
        mes_ano = self.mes_ano_entry.get()
        horas_trabalhadas = self.horas_trabalhadas_entry.get()
        valor_pago = self.valor_pago_entry.get()

        if not funcionario_id or not mes_ano or not horas_trabalhadas or not valor_pago:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Folha_Pagamento (funcionario_id, mes_ano, horas_trabalhadas, valor_pago) VALUES (%s, %s, %s, %s)",
                (funcionario_id, mes_ano, horas_trabalhadas, valor_pago)
            )
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Registro de folha salvo!")
            self.limpar_campos_folha()
            self.carregar_dados_folha()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def editar_folha(self):
        selected_item = self.tree_folha.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um registro para editar!")
            return

        funcionario_id = self.funcionario_id_entry.get()
        mes_ano = self.mes_ano_entry.get()
        horas_trabalhadas = self.horas_trabalhadas_entry.get()
        valor_pago = self.valor_pago_entry.get()

        if not funcionario_id or not mes_ano or not horas_trabalhadas or not valor_pago:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            id_folha = self.tree_folha.item(selected_item, 'text')
            self.cursor.execute(
                "UPDATE Folha_Pagamento SET funcionario_id = %s, mes_ano = %s, horas_trabalhadas = %s, valor_pago = %s WHERE id = %s",
                (funcionario_id, mes_ano, horas_trabalhadas, valor_pago, id_folha)
            )
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Registro de folha atualizado!")
            self.limpar_campos_folha()
            self.carregar_dados_folha()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar: {e}")

    def excluir_folha(self):
        selected_item = self.tree_folha.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir!")
            return

        try:
            id_folha = self.tree_folha.item(selected_item, 'text')
            self.cursor.execute("DELETE FROM Folha_Pagamento WHERE id = %s", (id_folha,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Registro de folha excluído!")
            self.limpar_campos_folha()
            self.carregar_dados_folha()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir: {e}")

    def carregar_dados_folha(self):
        self.tree_folha.delete(*self.tree_folha.get_children())
        self.cursor.execute("SELECT id, funcionario_id, mes_ano, horas_trabalhadas, valor_pago FROM Folha_Pagamento")
        for row in self.cursor.fetchall():
            self.tree_folha.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4]))

    def preencher_campos_folha(self, event):
        selected_item = self.tree_folha.selection()
        if selected_item:
            values = self.tree_folha.item(selected_item, 'values')
            self.funcionario_id_entry.delete(0, END)
            self.funcionario_id_entry.insert(0, values[0])
            self.mes_ano_entry.delete(0, END)
            self.mes_ano_entry.insert(0, values[1])
            self.horas_trabalhadas_entry.delete(0, END)
            self.horas_trabalhadas_entry.insert(0, values[2])
            self.valor_pago_entry.delete(0, END)
            self.valor_pago_entry.insert(0, values[3])

    def limpar_campos_folha(self):
        self.funcionario_id_entry.delete(0, END)
        self.mes_ano_entry.delete(0, END)
        self.horas_trabalhadas_entry.delete(0, END)
        self.valor_pago_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = AppCRUD(root)
    root.mainloop()


    