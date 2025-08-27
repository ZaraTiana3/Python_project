import heapq
import copy 
 #Using 6 tubes but with negative heapq 

from itertools import takewhile


class Tube:
    def __init__(self, tube):
        self.t = tube
        self.count=0 #variable pour suivre trace les tubes
        self.state=[-2,-2, -2, -2, -2, -2,-2, -2,-2, 0,0] #-2 Mixed, #-1 Spaced, #0 Empty, #1 Correct
    
    def print_tube(self):
        #Pour afficher l'état des tubes
        for i in range(NIVEAU):
            ligne = " ".join(f"|{self.t[col][i]}|" for col in range(len(self.t)))
            print(ligne)

def determine_filler(tube, avoid_positions:list, pos_filled:list, qtt_filled:int, clr_filled:list):
#Cette section sert a determiner le tube  filler(celui qui remplit) pour un espace blanc
#avoid_positions contient les tubes a ne pas considérer car ce sont des tubes vides ou le candidat lui-meme ou tube bien rempli
    qtt_filler=-1
    pos_filler=-1
    niveau_filler=-1
    avoid_positions=avoid_positions+[pos_filled] 
    clr=-1
    if clr_filled[0]==' ': #'Si la couleur est espace(cad que la tube est entierement vide), on peut prendre ttes les clrs possible'
        clr_filled = ALL_COLOR
    for i,t in enumerate(tube):#parcourir les tubes
        if i in avoid_positions: #ignorer les tubes incluses dans all_position
            continue
        for j, couleur in enumerate(t): #parcourir les couleurs
            if couleur==' ': #Tant que la place est encore vide, procéder aux  niveaux suivants
                continue
            if couleur in clr_filled:        
                count= sum(1 for x in takewhile(lambda x: x == couleur, t[j:]))  
                if j+count==NIVEAU and qtt_filled==NIVEAU: 
                   
                    break
    #if count>qtt_filler: ceci veut dire que si la nvelle vlr count est > à qtt_filler , qtt_filler est mis à jour
                if (count > qtt_filler) and (qtt_filled>=count):
    #Si qtt_filled(tube a remplir)>=count(celui qui remplit),cad le filler rentre bien dans filled, qtt_filler est mis a jour 
                    clr=couleur #clr désigne la couleur à retourner
                    qtt_filler=count  #qtt_filler désigne la quantité du filler
                    pos_filler=i    #position du filler
                    niveau_filler=j
            break #quand on a recupéré la couleur au debut d'un nieme tube et pourtant sans resultat, on passe au prochain(n+1) tube
        else:
            continue
    return pos_filler, qtt_filler, niveau_filler, clr


def check_result(t):
    somme = sum(i for i in t.state)
    return somme==TUBE


def determine_candidates(t, space:list): #candidates is the  postion_to_fill(contain white space)
    res =[]
    qtt=0 #space contain list of tubes with space 
    for i, t  in enumerate(t.t):
        if i not in space: 
            continue
        qtt = t[0:NIVEAU].count(' ')
        if qtt==4:
            for c in ALL_COLOR:
                res.append([-qtt, i, c]) #faire une liste pour une position et chaque couleur possible
        else:
            res.append([-qtt, i, t[qtt]]) #i: position, qtt: quantite libre
    return res

def evaluate_state(t, pos, clr):
    if t.t[pos][0]==' ':#si le début est vide 
        if  t.t[pos][NIVEAU-1]!=' ' :#vide au debut mais rempli au fond 
            t.state[pos] = -1
        elif t.t[pos][NIVEAU-1]==' ': #totalement vide
            t.state[pos] = 0
    elif t.t[pos][0]!=' ':#si le tube est rempli
        if sum(1 for j in range(NIVEAU) if t.t[pos][j]==clr)==NIVEAU: #toutes les couleurs sont les meme 
            t.state[pos]=1
        else:#les couleurs sont différentes 
            t.state[pos]=-2


def fill_modify(t, niveau_filler, clr_filled:str, pos_filler:int,pos_filled:int, qtt_filler:int, qtt_filled:int):
    #remplir la case vide à la pos_filled avec la couleur clr_filled a la position pos_filler
    #On commence a remplir a partir de first_to_fill jusqu'a last_to_fill
    first_to_fill = qtt_filled-qtt_filler 
    last_to_fill = qtt_filled #niveau last_to_fill non inclus
    
    #Remplir les cases vides() du to_fill
    for i in range(first_to_fill, last_to_fill):
        t.t[pos_filled][i]=clr_filled

    #Enlever les couleurs du filler, qtt_filler
    for i in range(niveau_filler, niveau_filler+qtt_filler): #niveau qtt_filler non inclus
        t.t[pos_filler][i]=' '

    #Evaluate the state of the tube 
    evaluate_state(t, pos_filler, clr_filled)
    
     #Evaluate the state of the tube 
    evaluate_state(t, pos_filled, clr_filled)
    #print(t.state)


    
def cancel_move(t, niveau_filler,clr_filled:str, pos_filler:int,pos_filled:int, qtt_filler:int, qtt_filled:int):
    #remplir la case vide à la pos_filled avec la couleur clr_filled a la position pos_filler
    #On commence a remplir a partir de first_to_fill jusqu'a last_to_fill
    first_to_fill = qtt_filled-qtt_filler 
    last_to_fill = qtt_filled #niveau last_to_fill non inclus

    #Remplir les cases vides() du to_fill
    for i in range(first_to_fill, last_to_fill):
        t.t[pos_filled][i]=' '

    #Enlever les couleurs du filler, qtt_filler
    for i in range(niveau_filler, niveau_filler+qtt_filler): #niveau qtt_filler non inclus
        t.t[pos_filler][i]=clr_filled

    evaluate_state(t, pos_filler, clr_filled)
 
    evaluate_state(t, pos_filled, clr_filled)


def solve(t, k, dic):
     
    k+=1
    
    dic[k] = copy.deepcopy(t.t)

    if sum(i for i in t.state)==TUBE-2:
        t.print_tube() 
        for k, v in dic.items():
            print(k)
            for i in range(NIVEAU):
                ligne = " ".join(f"|{v[col][i]}|" for col in range(len(v)))
                print(ligne)

        return True
    

    space =  [i for i, val in enumerate(t.state) if val == 0 or val==-1]#all  tubes with  white space
    pos_to_avoid= [i for i, val in enumerate(t.state) if val == 0 or val==1] #contain all empty space
    candidates = determine_candidates(t, space) #qtt, pos, clr
    heapq.heapify(candidates)
    

    while candidates:
        qtt_filled,pos_filled, clr_filled = heapq.heappop(candidates)
        qtt_filled = -qtt_filled
        #all_positions est la position_exclue
        pos_filler, qtt_filler, niveau_filler, clr_filled = determine_filler(t.t, pos_to_avoid, pos_filled, qtt_filled,clr_filled)
        if pos_filler==-1:
            continue
        fill_modify(t, niveau_filler, clr_filled, pos_filler,pos_filled, qtt_filler, qtt_filled)
        #Afficher l'etat actuel du tube
        if solve(t, k, dic):
            return True
        cancel_move(t, niveau_filler, clr_filled, pos_filler,pos_filled, qtt_filler, qtt_filled)
    return False


TUBE = 11
NIVEAU = 4

t = [['c','k','k','r'],['m','w','b','b'],['w','w','p','g'],['b','g','m','r'],['c','o','r','m'],
      ['c','g','p','c'],['p','p','o','r'],['o','b','o','m'], ['g','k','w','k'],[' ']*NIVEAU,[' ']*NIVEAU]


ALL_COLOR = []

for i in t:
   for j in i:
    if j not in ALL_COLOR and j!=' ':
        ALL_COLOR.append(j)
        if len(ALL_COLOR)==TUBE-2:
            break



t = Tube(t)
t.print_tube()
k=0
print('We begin')
dic = {}
solve(t,k, dic)

 





    