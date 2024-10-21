# !pip install supabase

# ou 

# pip install supabase

import os
from datetime import datetime
import uuid
import re
from supabase import create_client, Client
supabase: Client = create_client("https://brioutndycetdzaqsxka.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyaW91dG5keWNldGR6YXFzeGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NjIxNDgsImV4cCI6MjAyOTEzODE0OH0.fE2ANGfCaVLTaFZMb8d43WUEqOsCiURSL-NRjXO4ga0")

id = ''
# defino id = '', afinal, vou usa-lo como parâmetro mais tarde, então ja defino como um valor "nulo" desde já

def limparPrompt() :
    if os.name == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def listarUsuariosCadastrados(usuariosCadastrados) :
  response = supabase.table("usuarios").select("*").execute().data

  for i in range(len(response)) :
    usuariosCadastrados.append({
      'id' : response[i]['id'],
      'email' : response[i]['email'],
      'name' : response[i]['name'],
      'user_name' : response[i]['user_name'],
      'password' : response[i]['password']
        })


usuariosCadastrados = []
listarUsuariosCadastrados(usuariosCadastrados)


def verificarEmail (email) :
  validacao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
  if(re.fullmatch(validacao, email)):
   
    return True
  else:
    return False


def cadastrar() :
    # try :
        usuariosCadastrados = []
        listarUsuariosCadastrados(usuariosCadastrados)

        id = str(uuid.uuid4())
        email = input('Digite seu email: ')
        if verificarEmail(email) != True :
            print('Email inválido, tente novamente.')
            cadastrar()

        name = input('Digite seu nome completo: ')
        user_name = input('Digite seu user_name: ')

        for i in usuariosCadastrados :
            if i['email'] ==  email or i['user_name'] ==  user_name :
                print('Email ou nome de usuário já cadastrado , tente outro.')
                cadastrar()

        tamanho_user_name = len(user_name)

        if tamanho_user_name >= 40 or tamanho_user_name <= 5 :
            print('O nome de usuário deve conter entre 5 e 20 caracteres')

        password = input('Digite sua senha: ')

        if len(password) <= 6 :
            print('A senha deve conter no mínimo 6 caracteres')
            cadastrar()
        elif len(password) > 16 :
            print('A senha não pode ter mais que 16 caracteres')
            cadastrar()

        supabase.table("usuarios").insert({"id": id , "email" : email ,"name": name , "user_name":user_name , "password" :password }).execute()

        print('Usuário cadastrado com sucesso!')

    # except:
    #     print('Houve um erro\nTente novamente mais tarde')
    #     cadastrar()

def login(id) :
    user_name = input('Digite seu user name: ')
    password = input('Digite sua senha: ')
    response = supabase.table("usuarios").select("*").eq("user_name" , user_name ).eq("password" , password).execute().data

    if user_name != response[0]['user_name'] or password != response[0]['password'] :
        print('Usuário Não Cadastrado, ou senha/user name incorreta.')
        return login()

    print(response[0]['email'] , " -- " , response[0]['user_name'] , " -- Logado com sucesso")

    id = response[0]['id']
    return id

  
    

def mostrarUsuarios () :
  todosUsuarios = supabase.table("usuarios").select("*").execute().data

  for i in range (len(todosUsuarios)) :
    user = todosUsuarios[i]['user_name']

    print("(",(i+1) , ") ", user)

  return

def comentarComUsuario () :
    usuarioId = ''
    comment = 'sair' 
    # condição para sair da aba de comentários

    userId = login(usuarioId)

    mostrarUsuarios()

    usuariosCadastrados = []
    listarUsuariosCadastrados(usuariosCadastrados)
    

    for i in range(len(usuariosCadastrados)) :
        if userId == usuariosCadastrados[i]['id'] :
            comment_owner = usuariosCadastrados[i]['user_name']
            break

    escolhaUsuarios = int(input('Escolha um usuario para conversar: '))
    limparPrompt()
    
    print("Digite 'sair' quando quiser sair da aba de comentários!")
    while comment == 'sair' :
        for i in range(len(usuariosCadastrados)) :
            if escolhaUsuarios == (i+1) :
                other_user = usuariosCadastrados[i]['id']
                todosComentarios = supabase.table('comentarios').select('*, usuarios!inner(user_name)').eq('other_user' , other_user).execute().data

                print(usuariosCadastrados[i]['user_name'] , " :")
                for i in todosComentarios :
                   print(i['usuarios']['user_name'] , ' :',i['comment'])

                id = str(uuid.uuid4())
                comment = input('Deixe seu comentário: ')
                
                if comment == 'sair' :
                   return run()
                   
                commented_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                supabase.table("comentarios").insert({"id": id , "comment_owner" : comment_owner , "comment" : comment , "commented_at" : commented_at , "other_user" : other_user}).execute()
                limparPrompt()
        
        # else :
        #     print('Opção Invalida.')
        #     comentarComUsuario(id)

        



def menu () :
    print('1: Login')
    print('2: Cadastrar')
    print('3: Conversar com usuario - Login necessário')
    print('4: Sair')

    opcao = int(input('Escolha uma opção: '))
    return opcao


def run () :
  limparPrompt()
  while True:
    # try
      match menu():
        case 1 :
          login(id)
          print('Logado com sucesso!')
          limparPrompt()
          run()

        case 2:
          print('Cadastrando...')
          cadastrar()
          limparPrompt()
          run()

        case 3:
          limparPrompt()
          comentarComUsuario()

        case 4:
          print('Saindo... Espero ve-lo em breve!')
          limparPrompt()
          break
          
          
        case _:
          print('Opção inválida')
          continue

    # except:
    #   print('Tente novamente')

run()