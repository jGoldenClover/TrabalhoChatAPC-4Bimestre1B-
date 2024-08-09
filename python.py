
def organizarOrdemCrescente (pontos ) :

#  [roberto , alexandre , valdemir] -- lista de nomes correspondente aos pontos
#  [20 , 15 , 1] -- vetor  de pontos
#    0   1    2   -- indice dos vetores

   i = 1

   while i < len(pontos) :      
# 'indice Atual' é só pra diferenciar de i

         #1º interação           #2º interacao       #3º interação -- o itemAtual é menor que o itemAnterior então o else para as 3 interações do while

      indiceAtual = i  # indiceAtual = 1        #indiceAtual = 2
      itemAtual = pontos[i] # itemAtual = 15       #itemAtual = 1
      nomeAtual = nomes[i]  #nomeAtual = alexandre       #nomeAtual = valdemir

      # não uso o i no lugar do IndiceAtual por que eu mudo o valor de (i) 2 vezes no codigo e isso acabava me confundindo eventualmente
      while indiceAtual > 0 :                                           

#                                        #1 volta só nessa interação       #1º volta no while            #2º volta no while 
         indiceAnterior = indiceAtual - 1 #indiceAnterior =  0             #indiceAnterior = 1           # IndiceAnterior = 0 , indiceAtual = 1
         itemAnterior = pontos[indiceAnterior] #itemAnterior = 20          #itemAnterior = 20            #itemAnterior = 15 , itemAtual = 1
         nomeAnterior = nomes[indiceAnterior] 

         if itemAtual > itemAnterior:           
            pontos[indiceAtual] = itemAnterior #[15 , 15 , 1]              #[15 , 20 , 20]               #[15 , 15 , 20]
            nomes[indiceAtual] = nomeAnterior  
            indiceAtual -= 1  
# subtraio o indice para satisfazer a condição do while e continuar o código

#quando o itemAtual tiver o mesmo valor que o item anterior, como o acontecido na primeira interação então a gente para o loop
         else:
            break
      
      pontos[indiceAtual] = itemAtual  #indiceAtual = 0 itemAtual = 15  ----- [15  ,20 , 1] 
#                                      #indiceAtual = 0 itemAtual = 1  ----- [1 , 15 , 20]
      nomes[indiceAtual] = nomeAtual   

      i += 1 


nomes = []
pontos =[]

for i in range(3) :
   nome = input("Digite o nome do atleta : ")
   pontosAtleta = int(input("Digite a pontuação do atleta : "))
   print(" \n ------ Paris 2024 ------ \n")

   nomes.append(nome)
   pontos.append(pontosAtleta)

print(pontos , nomes)

organizarOrdemCrescente(pontos)


print("\nOuro:" , pontos[0] , nomes[0] , "\nPrata:" , pontos[1] , nomes[1]  , "\nBronze:" , pontos[2] , nomes[2] )


