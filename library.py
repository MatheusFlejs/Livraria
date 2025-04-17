import tkinter as tk
from tkinter import ttk
from datetime import date
from PIL import Image,ImageTk
import requests
from io import BytesIO

class usuario:
    def __init__(self,nome,id,endereco,telefone):
        self.nome = nome
        self.id = id
        self.endereço = endereco
        self.telefone = telefone
    def pesquisar(self,tree):
        tree.delete(*tree.get_children())
        tree.insert("","end",values=(self.nome,self.id,self.endereço,self.telefone))
    def cadastrar(self,tree):
        tree.insert("","end",values=(self.nome,self.id,self.endereço,self.telefone))

class livro:
    def __init__(self,titulo,autor,ISBN,id,imagem_url,disponibilidade=True):
        self.titulo = titulo
        self.autor = autor
        self.ISBN = ISBN
        self.id = id
        self.imagem_url = imagem_url
        self.disponibilidade = disponibilidade
    def cadastrar(self,tree,image_label):
        tree.insert("","end",values=(self.titulo,self.autor,self.ISBN,self.id,self.disponibilidade))
        self.mostrar_imagem(image_label)
    def pesquisar(self,tree,imagem_label):
        tree.delete(*tree.get_children())
        tree.insert("","end",values=(self.titulo,self.autor,self.ISBN,self.id,self.disponibilidade))
        self.mostrar_imagem(imagem_label)
    def mostrar_imagem(self,image_label):
        try: 
            response = requests.get(self.imagem_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((150,200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image=photo
        except Exception as e :
            image_label.config(text="imagem nao encontrada")
            image_label.img=""

class emprestimo:
    def __init__(self,dataEmprestimo,dataDevolucao,livro,usuario):
        self.dataEmprestimo = dataEmprestimo
        self.dataDevolucao = dataDevolucao
        self.status = "Emprestado"
        self.livro = livro
        self.usuario = usuario
    def realizar_emprestimo(self,tree):
        if self.livro.disponibilidade:
            self.livro.disponibilidade = False
            tree.insert("","end",values=(self.livro.titulo,self.usuario.nome,self.dataEmprestimo,self.dataDevolucao))
        else:
            print("Livro nao encontrado")

    def realizar_Devolucao(self,tree):
        self.livro.disponibilidade = True
        self.status = "Devolvido"
        tree.insert("","end",values=(self.livro.titulo,self.usuario.nome,self.dataEmprestimo,self.dataDevolucao,self.status))

#class bibliotecario:

class relatorio:
    def __init__(self,tipo_relatorio):
        self.tipo_relatorio = tipo_relatorio
        self.data_geracao = date.today()
    def gerar_relatorio(self):
        print("Relatório ",{self.tipo_relatorio}," gerado em {self.data_geracao}")

def main():
    window = tk.Tk()
    window.title("Sistema de Gerenciamento de Biblioteca")

    image_Label = tk.Label(window)
    image_Label.grid(row=5, column=0, rowspan=3)

    usuario_tree = ttk.Treeview(window,columns=('Nome','Id','Endereco','Telefone'),show="headings")
    usuario_tree.heading('Nome',text='Nome')
    usuario_tree.heading('Id',text='Id')
    usuario_tree.heading('Endereco',text='Endereco')
    usuario_tree.heading('Telefone',text='Telefone')
    usuario_tree.grid(row=0,column=0,padx=10,pady=10)

    emprestimo_tree = ttk.Treeview(window,columns=('Livro','Usuario','Data Emprestimo','Data Devolução', 'Status'),show='headings')
    
    emprestimo_tree.heading('Livro',text='Livro')
    emprestimo_tree.heading('Usuario',text='Usuario')
    emprestimo_tree.heading('Data Emprestimo',text='Data Emprestimo')
    emprestimo_tree.heading('Data Devolução',text='Data Devolução')
    emprestimo_tree.heading('Status',text='Status')
    emprestimo_tree.grid(row=5,column=2,columnspan=2,padx=10,pady=10)

    livro_tree = ttk.Treeview(window,columns=('Titulo','Autor','ISBN','ID','Disponibilidade'),show='headings')

    livro_tree.heading('Titulo',text='Titulo')
    livro_tree.heading('Autor',text='Autor')
    livro_tree.heading('ISBN',text='ISBN')
    livro_tree.heading('ID',text='ID')
    livro_tree.heading('Disponibilidade',text='Disponibilidade')
    livro_tree.grid(row=0,column=2,padx=10,pady=10)

    usuario1 = usuario("João Silva",1,"Rua A, 123","4398800-0088")
    livro1 = livro("A Odisseia","Homero","978-012345",101,"https://glorificai.com/cdn/shop/products/Studio-Project-2022-01-14T182831.036_580x.png?v=1642203248")
    livro2 = livro("Ilíada","Homero","978-012345",102,"https://glorificai.com/cdn/shop/products/Studio-Project-2022-01-14T182503.854_1200x1200.png?v=1642202848")
    livro3 = livro("O Livro dos Espiritos", "Kardec, Allan","978-012345",103,"https://candeia.vteximg.com.br/arquivos/ids/212407-1000-1000/18975.png?v=637822629776800000")
    livro4 = livro("O Livro dos Mediuns", "Kardec, Allan","978-012345",104,"https://candeia.vteximg.com.br/arquivos/ids/222992-1000-1000/3988.png?v=638252855140830000")
    livro5 = livro("O Pensamento de Immanuel Kant", "González, Mário", "978-012345",105,"https://glorificai.com/cdn/shop/files/280985-1_360x.webp?v=1687893282 ")

    usuario1.cadastrar(usuario_tree)
    livro1.cadastrar(livro_tree,image_Label)
    livro2.cadastrar(livro_tree,image_Label)
    livro3.cadastrar(livro_tree,image_Label)
    livro4.cadastrar(livro_tree,image_Label)
    livro5.cadastrar(livro_tree,image_Label)

    emprestimo1 = emprestimo(date(2024,2,20),date(2024,3,20),livro1,usuario1)
    emprestimo2 = emprestimo(date(2025,2,20),date(2025,3,20),livro2,usuario1)
    

    emprestimo1.realizar_emprestimo(emprestimo_tree)
    emprestimo2.realizar_emprestimo(emprestimo_tree)
    emprestimo1.realizar_Devolucao(emprestimo_tree)
    relatorio1 = relatorio("Emprestimos")
    relatorio1.gerar_relatorio()
    usuario1.pesquisar(usuario_tree)

    def livro_selecionado(event):
        item = livro_tree.selection()
        if item:
            item_id = item[0]
            values = livro_tree.item(item_id,'values')
            if values:
                livro_id = int(values[3])
                if livro_id == livro1.id:
                    livro = livro1
                elif livro_id == livro2.id:
                    livro = livro2
                elif livro_id == livro3.id:
                    livro = livro3
                elif livro_id == livro4.id:
                    livro = livro4
                elif livro_id == livro5.id:
                    livro = livro5
                else:
                    print("Livro não encontrado")
                    return
            image_Label.config(image="")
            image_Label.image = None
            livro.mostrar_imagem(image_Label)
    livro_tree.bind("<ButtonRelease-1>",livro_selecionado)
    window.mainloop()

if __name__ == "__main__":
    main()

    

