import time
import pygame
import sys
import math


def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    GOL = '#'
    noduri = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)
    ]
    muchii = [(0, 1), (1, 2), (2, 3), (3, 4),  # linii verticale
                  (5, 6), (6, 7), (7, 8), (8, 9),
                  (10, 11), (11, 12), (12, 13), (13, 14),
                  (15, 16), (16, 17), (17, 18), (18, 19),
                  (20, 21), (21, 22), (22, 23), (23, 24),
                  (0, 5), (5, 10), (10, 15), (15, 20),  # linii orizontale
                  (1, 6), (6, 11), (11, 16), (16, 21),
                  (2, 7), (7, 12), (12, 17), (17, 22),
                  (3, 8), (8, 13), (13, 18), (18, 23),
                  (4, 9), (9, 14), (14, 19), (19, 24),
                  (0, 6), (6, 10), (10, 16), (16, 20),  # linii diagonale
                  (2, 6), (6, 12), (12, 16), (16, 22),
                  (2, 8), (8, 12), (12, 18), (18, 22),
                  (4, 8), (8, 14), (14, 18), (18, 24)
    ]
    scalare = 100
    translatie = 20
    raza_pct = 10
    raza_piesa = 20


    @classmethod
    def initializeaza(cls, display):
        cls.display = display
        cls.diametru_piesa = 2 * cls.raza_piesa
        cls.piesa_alba = pygame.image.load('piesa-alba.png')
        cls.piesa_alba = pygame.transform.scale(cls.piesa_alba, (cls.diametru_piesa, cls.diametru_piesa))
        cls.piesa_neagra = pygame.image.load('piesa-neagra.png')
        cls.piesa_neagra = pygame.transform.scale(cls.piesa_neagra, (cls.diametru_piesa, cls.diametru_piesa))
        cls.piesa_rosie = pygame.image.load('piesa-rosie.png')
        cls.piesa_rosie = pygame.transform.scale(cls.piesa_rosie, (cls.diametru_piesa, cls.diametru_piesa))


        cls.culoare_ecran = (255, 255, 255)
        cls.culoare_linii = (0, 0, 0)
        cls.coordonate_noduri = [[cls.translatie + cls.scalare * x for x in nod] for nod in cls.noduri]



    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]
        self.display.fill(self.culoare_ecran)
        for nod in self.coordonate_noduri:
            pygame.draw.circle(surface=self.display, color=self.culoare_linii, center=nod, radius=self.raza_pct,
                               width=0)  # width=0 face un cerc plin

        for muchie in self.muchii:
            p0 = self.coordonate_noduri[muchie[0]]
            p1 = self.coordonate_noduri[muchie[1]]
            pygame.draw.line(surface=self.display, color=self.culoare_linii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.piese_albe:
            self.display.blit(self.piesa_alba, (nod[0] - self.raza_piesa, nod[1] - self.raza_piesa))
        for nod in self.piese_negre:
            self.display.blit(self.piesa_neagra, (nod[0] - self.raza_piesa, nod[1] - self.raza_piesa))
        if self.nod_piesa_selectata:
            self.display.blit(self.piesa_rosie, (self.nod_piesa_selectata[0] - self.raza_piesa, self.nod_piesa_selectata[1] - self.raza_piesa))
        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

    # pygame.display.update()

    def __init__(self, piese_albe = None, piese_negre = None, capturat = False, nod_piesa_selectata = None):
        self.capturat = capturat
        self.coordonate_noduri = [[self.translatie + self.scalare * x for x in nod] for nod in self.noduri]

        self.piese_albe = piese_albe or [
            self.coordonate_noduri[3], self.coordonate_noduri[4],
            self.coordonate_noduri[8], self.coordonate_noduri[9],
            self.coordonate_noduri[13], self.coordonate_noduri[14],
            self.coordonate_noduri[17], self.coordonate_noduri[18], self.coordonate_noduri[19],
            self.coordonate_noduri[22], self.coordonate_noduri[23], self.coordonate_noduri[24]
        ]
        self.nod_piesa_selectata = nod_piesa_selectata
        self.piese_negre = piese_negre or [
            self.coordonate_noduri[0], self.coordonate_noduri[1], self.coordonate_noduri[2],
            self.coordonate_noduri[5], self.coordonate_noduri[6], self.coordonate_noduri[7],
            self.coordonate_noduri[10], self.coordonate_noduri[11],
            self.coordonate_noduri[15], self.coordonate_noduri[16],
            self.coordonate_noduri[20], self.coordonate_noduri[21]
        ]


    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def pot_muta(self, piesa, jucator):
        index = self.coordonate_noduri.index(piesa)
        for i in [index - 6, index - 5, index - 4, index - 1, index + 1, index + 4, index + 5, index + 6]:
            if 0 <= i < 25:
                loc = self.coordonate_noduri[i]
                if (index, i) in self.muchii or (i, index) in self.muchii:
                    if loc not in self.piese_albe + self.piese_negre:
                        return True

        piese_curente = self.piese_albe
        piese_adverse = self.piese_negre
        if jucator == 'negre':
            piese_curente, piese_adverse = piese_adverse, piese_curente
        for i in [-12, -10, -8, -2, 2, 4, 10, 12]:
            mij = int(index + i / 2)
            varf = index + i
            if 0 <= mij < 25 and 0 <= varf < 25 and self.e_muchie(index, mij) and self.e_muchie(mij, varf):
                if self.coordonate_noduri[mij] in piese_adverse and self.coordonate_noduri[
                    varf] not in piese_adverse + piese_curente:
                    return True
        return False

    def final(self):
        if len(self.piese_albe) == 0:
            return "negre"
        if len(self.piese_negre) == 0:
            return "albe"
        ok = False
        for piesa in self.piese_albe:
            if self.pot_muta(piesa, "albe"):
                ok = True
                break
        if not ok:
            return "negre"
        ok = False
        for piesa in self.piese_negre:
            if self.pot_muta(piesa, "negre"):
                ok = True
                break
        if not ok:
            return "albe"
        return False

    def e_muchie(self, index1, index2):
        return (index1, index2) in self.muchii or (index2, index1) in self.muchii

    def mutari(self, jucator_opus):
        l_mutari = []
        piese_curente = self.piese_albe
        piese_adverse = self.piese_negre
        if self.JMAX == 'negre':
            piese_curente, piese_adverse = piese_adverse, piese_curente
        for piesa in piese_curente:
            index = self.coordonate_noduri.index(piesa)
            for i in [-12, -10, -8, -2, 2, 4, 10, 12]:
                mij = int(index + i/2)
                varf = index + i
                if 0 <= mij < 25 and 0 <= varf < 25 and self.e_muchie(index, mij) and self.e_muchie(mij, varf):
                    if self.coordonate_noduri[mij] in piese_adverse and self.coordonate_noduri[varf] not in piese_adverse + piese_curente:
                        piese_curente_noi = list(piese_curente)
                        piese_curente_noi.remove(piesa)
                        piese_curente_noi.append(self.coordonate_noduri[varf])
                        piese_adverse_noi = list(piese_adverse)
                        piese_adverse_noi.remove(self.coordonate_noduri[mij])
                        if self.JMAX == 'negre':
                            l_mutari.append(Joc(piese_adverse_noi, piese_curente_noi, True))
                        else:
                            l_mutari.append(Joc(piese_curente_noi, piese_adverse_noi, True))
            for i in [index - 6, index - 5, index - 4, index - 1, index + 1, index + 4, index + 5, index + 6]:
                if 0 <= i < 25:
                    loc = self.coordonate_noduri[i]
                    if self.e_muchie(i, index):
                        if loc not in piese_curente + piese_adverse:
                            piese_curente_noi = list(piese_curente)
                            piese_curente_noi.remove(piesa)
                            piese_curente_noi.append(loc)
                            if self.JMAX == 'negre':
                                l_mutari.append(Joc(piese_adverse, piese_curente_noi))
                            else:
                                l_mutari.append(Joc(piese_curente_noi, piese_adverse))
        return l_mutari


    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus

    def linie_deschisa(self, piesa, jucator):
        scor = 0
        index = self.coordonate_noduri.index(piesa)
        piese_curente = self.piese_negre
        piese_adverse = self.piese_albe
        if jucator == 'albe':
            piese_curente, piese_adverse = piese_adverse, piese_curente
        for i in [-12, -10, -8, -2, 2, 4, 10, 12]:
            mij = int(index + i/2)
            varf = index + i
            if 0 <= mij < 25 and 0 <= varf < 25 and self.e_muchie(index, mij) and self.e_muchie(mij, varf):
                if self.coordonate_noduri[mij] in piese_adverse:
                    piese_curente_noi = list(piese_curente)
                    piese_curente_noi.remove(piesa)
                    piese_curente_noi.append(self.coordonate_noduri[varf])
                    piese_adverse_noi = list(piese_adverse)
                    piese_adverse_noi.remove(self.coordonate_noduri[mij])
                    scor += 1
        return scor


    def linii_deschise(self, jucator):
        scor = 0
        if jucator == 'negre':
            for piesa in self.piese_negre:
                scor += self.linie_deschisa(piesa, jucator)
        else:
            for piesa in self.piese_albe:
                scor += self.linie_deschisa(piesa, jucator)
        return scor

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def __str__(self):
        sir = ""
        endl = 0
        for lin in range(5):
            for col in range(0,21,5):
                x = self.coordonate_noduri[col+lin]
                endl += 1
                if x in self.piese_negre:
                    sir += "N"
                elif x in self.piese_albe:
                    sir += "A"
                else:
                    sir += "G"
                if endl % 5 == 0:
                    sir += "\n"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    global n_min, n_max, n_l, mutari_gen  # noduri
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    mutari_gen += len(stare.mutari_posibile)


    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    global n_min, n_max, n_l, mutari_gen  # noduri
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare
    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez
    stare.mutari_posibile = stare.mutari()
    mutari_gen += len(stare.mutari_posibile)


    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)
            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break
    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)
            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare
    return stare

def afis():
    global t_min, t_max, t_l, n_min, n_max, n_l, timp, mutari_juc, mutari_pc
    if t_min != float('inf'):
        print("Timpul minim de gandire al calculatorului: " + str(t_min) + " milisecunde")
    if t_max != float('-inf'):
        print("Timpul maxim de gandire al calculatorului: " + str(t_max) + " milisecunde")
    if len(t_l):
        print("Timpul mediu de gandire al calculatorului: " + str(sum(t_l) / len(t_l)) + " milisecunde")
        sorted(t_l)
        mid = int((len(t_l) + 1) / 2)
        print("Timpul median de gandire al calculatorului: " + str(t_l[mid]) + " milisecunde\n")
    if n_min != float('inf'):
        print("Numarul minim de mutari generate: " + str(n_min))
    if n_max != float('-inf'):
        print("Numarul maxim de mutari generate: " + str(n_max))
    if len(n_l):
        print("Numarul mediu de mutari generate: " + str(sum(n_l) / len(n_l)))
        sorted(n_l)
        mid = int((len(n_l) + 1) / 2)
        print("Numarul median de mutari generate: " + str(n_l[mid]) + "\n")

    timp = int(round(time.time())) - timp
    print("Timpul total jucat: " + str(timp) + " secunde")
    print("Jucatorul a facut " + str(mutari_juc) + " mutari")
    print("Calculatorul a facut " + str(mutari_pc) + " mutari")
    return True


def afis_daca_final(stare_curenta):
    if stare_curenta == "force quit":
        print("\nJocul a fost intrerupt!\n")
        return afis()
    else:
        final = stare_curenta.tabla_joc.final()
        if (final):
            print("\nA castigat jucatorul cu piesele " + final + "!!\n")
            return afis()

    return False


def coliniare (n0, n1):
    x = n0[0]
    y = n0[1]
    x1 = n1[0]
    y1 = n1[1]
    if x == x1 and abs(y-y1) == 200:
        y2 = abs(y+y1)/2
        return [x, y2]
    if y == y1 and abs(x-x1) == 200:
        x2 = abs(x+x1)/2
        return [x2, y]
    if abs(x-x1) == 200 and abs(y-y1) == 200:
        x2 = abs(x+x1)/2
        y2 = abs(y+y1)/2
        return [x2, y2]
    return False


def capturare(n0, n1, piese_adverse):
    n2 = coliniare(n0, n1)
    if n2 == False:
        return False
    if n1 not in piese_adverse and n2 in piese_adverse:
        return n2
    return False

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="albe", valoare="albe"),
            Buton(display=display, w=35, h=30, text="negre", valoare="negre")
        ],
        indiceSelectat=0)
    btn_incep = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=70, h=30, text="Incep EU", valoare="eu"),
            Buton(display=display, w=70, h=30, text="Incepe PC", valoare="pc")
        ],
        indiceSelectat=0)
    btn_dif = GrupButoane(
        top = 240,
        left = 30,
        listaButoane=[
            Buton(display=display, w=60, h=30, text="incepator", valoare="1"),
            Buton(display=display, w=60, h=30, text="mediu", valoare="2"),
            Buton(display=display, w=60, h=30, text="avansat", valoare="3")
        ],
        indiceSelectat= 2
    )

    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    btn_incep.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                afis_daca_final("force quit")
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_incep.selecteazaDupacoord(pos):
                            if not btn_dif.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.deseneaza_grid()
                                    return btn_juc.getValoare(), btn_alg.getValoare(), btn_incep.getValoare(), btn_dif.getValoare()
        pygame.display.update()


def main():
    # initializari timp

    global t_juc_inainte, t_min, t_max, t_l, n_min, n_max, n_l, timp, mutari_pc, mutari_juc, mutari_gen # timp, noduri si mutari
    t_juc_inainte = int(round(time.time() * 1000))
    t_min = n_min = float('inf')
    t_max = n_max = float('-inf')
    t_l = []
    n_l = []
    timp = int(round(time.time()))
    mutari_pc = mutari_juc = mutari_gen = 0

    # initializare tabla
    tabla_curenta = Joc();
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    # jucatorul incepe mereu primul


    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('Richiteanu Mihai-Sebastian - Alquerque')
    # dimensiunea ferestrei in pixeli
    ecran = pygame.display.set_mode(size=(502, 502))  # N *100+ N-1
    Joc.initializeaza(ecran)

    Joc.JMIN, tip_algoritm, incep, ADANCIME_MAX = deseneaza_alegeri(ecran, tabla_curenta)
    ADANCIME_MAX = int(ADANCIME_MAX)
    Joc.JMAX = 'albe' if Joc.JMIN == 'negre' else 'negre'

    if incep == "eu":
        stare_curenta = Stare(tabla_curenta, Joc.JMIN, ADANCIME_MAX)
    else:
        stare_curenta = Stare(tabla_curenta, Joc.JMAX, ADANCIME_MAX)

    de_mutat = False
    tabla_curenta.deseneaza_grid()

    while True:
        j_current = stare_curenta.j_curent
        if (j_current == Joc.JMIN):
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    afis_daca_final("force quit")
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # coordonatele clickului
                    for nod in Joc.coordonate_noduri:
                        if distEuclid(pos, nod) <= Joc.raza_pct:
                            if (j_current == 'albe'):
                                piesa = Joc.piesa_alba
                                piese_curente = stare_curenta.tabla_joc.piese_albe
                                piese_adverse = stare_curenta.tabla_joc.piese_negre
                            else:
                                piesa = Joc.piesa_neagra
                                piese_curente = stare_curenta.tabla_joc.piese_negre
                                piese_adverse = stare_curenta.tabla_joc.piese_albe
                            if nod not in piese_curente + piese_adverse:
                                if stare_curenta.tabla_joc.nod_piesa_selectata:
                                    n0 = stare_curenta.tabla_joc.coordonate_noduri.index(nod)
                                    n1 = stare_curenta.tabla_joc.coordonate_noduri.index(stare_curenta.tabla_joc.nod_piesa_selectata)
                                    piesa_capturata = capturare(nod, stare_curenta.tabla_joc.nod_piesa_selectata, piese_adverse)
                                    if piesa_capturata:
                                        piese_adverse.remove(piesa_capturata)
                                        piese_curente.remove(stare_curenta.tabla_joc.nod_piesa_selectata)
                                        piese_curente.append(nod)
                                        stare_curenta.tabla_joc.nod_piesa_selectata = False
                                        t_juc_dupa = int(round(time.time() * 1000))
                                        mutari_juc += 1
                                        print("Jucatorul a \"gandit\" timp de " + str(
                                            t_juc_dupa - t_juc_inainte) + " milisecunde.")
                                        afis_daca_final(stare_curenta)
                                    elif ((n0, n1) in Joc.muchii or (n1, n0) in Joc.muchii):
                                        piese_curente.remove(stare_curenta.tabla_joc.nod_piesa_selectata)
                                        piese_curente.append(nod)
                                        stare_curenta.tabla_joc.nod_piesa_selectata = False
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        t_juc_dupa = int(round(time.time() * 1000))
                                        mutari_juc += 1
                                        print("Jucatorul a \"gandit\" timp de " + str(
                                            t_juc_dupa - t_juc_inainte) + " milisecunde.")
                            else:
                                if nod in piese_curente:
                                    if stare_curenta.tabla_joc.nod_piesa_selectata:
                                        stare_curenta.tabla_joc.nod_piesa_selectata = False
                                    else:
                                        stare_curenta.tabla_joc.nod_piesa_selectata = nod

                            stare_curenta.tabla_joc.deseneaza_grid()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            print("Estimare stare curenta: " + str(stare_curenta.estimare))

            stare_curenta.tabla_joc.deseneaza_grid()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            t_calc = t_dupa - t_inainte
            print("Calculatorul a \"gandit\" timp de " + str(t_calc) + " milisecunde.")
            if t_calc < t_min:
                t_min = t_calc
            if t_calc > t_max:
                t_max = t_calc
            t_l.append(t_calc)

            print("Nr mutari generate: " + str(mutari_gen))
            if mutari_gen < n_min:
                n_min = mutari_gen
            if mutari_gen > n_max:
                n_max = mutari_gen
            n_l.append(mutari_gen)
            mutari_gen = 0

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            if not stare_curenta.tabla_joc.capturat:
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            else:
                afis_daca_final(stare_curenta)
                time.sleep(1)
            mutari_pc += 1
            t_juc_inainte = int(round(time.time() * 1000))


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()