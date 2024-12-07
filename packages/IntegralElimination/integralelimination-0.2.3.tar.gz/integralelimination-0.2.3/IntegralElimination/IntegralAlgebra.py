import sympy as sp
from ordered_set import OrderedSet
from IPython.display import display, Math

from .ordering import IMO
from .IntegralMonomial import IM
from .utils import (
    is_int,
    ShuffleList,
    diff_lists,
    dicts_addition,
    dicts_subtraction,
    dict_mul_by_coeff,
    expr_has_symbol
)
from .IntegralPolynomial import IntegralPolynomial
from .reduction import (
    reduction_M_by_P_simple_case,
    reduction_M_by_P_reduced_power, 
    reduction_M_by_P, 
    reduce,auto_reduce
)
from .critical_pairs import (
    critical_pairs_PI_QI,
    critical_pairs_PI_QN,
    critical_pairs_PN_QN,
    critical_pairs
)
from .exp_log import (
    find_A_A0_G_F, 
    update_exp, 
    update_log,
    extend_X_with_exp_and_log
) 
from .integral_elimination import integral_elimination

class IntegralAlgebra():
    """
    integral polynomials will be represented as follows :
    eq = {IM(x(t):3, IM(y(t),1,y(t)):theta+lambda}
    using eq.as_coefficients_dict(IM)
    It means that eq is the sum of the two tuples 
    """
    def __init__(self, order, parameters):
        self.order = order
        self.t = sp.Symbol("t")
        self.used_order = order
        self.used_order_str = str(order)
        self.IMO_le = lambda m1, m2 : IMO(m1, m2, self.used_order) 
        self.parameters = parameters
        self.storage = self.init_storage()

    def init_storage(self):
        storage = {
            "LM_LC": {},
            "P_red_to_zero": {}
        }
        return storage
    
    def update_IMO(self, order):
        self.used_order = order
        self.used_order_str = str(order)
        self.IMO = lambda m1, m2 : IMO(m1, m2, self.used_order)
 
    def LM_LC(self, P:IntegralPolynomial) -> tuple[IM, sp.Expr]:
        """
        get leading monomials and coeff
        """
        if P.is_zero():
            return None
        str_order = self.used_order_str
        if not self.storage["LM_LC"].get(str_order):
            self.storage["LM_LC"][str_order]={}
        if not self.storage["LM_LC"][str_order].get(P): 
            L = P.get_content() 
            LC, LM = L[0][1], L[0][0]
            for M,coeff in L:   
                #if True then M <= LM, else M > LM
                if self.IMO_le(M, LM) == False: 
                    LM = M # im > LM
                    LC = coeff
            self.storage["LM_LC"][str_order][P] = (LM,LC)
        LM, LC = self.storage["LM_LC"][str_order][P]
        return LM, LC
    
    def LM_LC_P_I(self, P:IntegralPolynomial) -> tuple[IM, sp.Expr]:
        if P.is_zero():
            return 
        P_I = P.get_P_I()
        if P_I.is_zero(): return None
        return self.LM_LC(P_I)
    
    def LM_LC_P_N(self, P:IntegralPolynomial) -> tuple[IM, sp.Expr]:
        if P.is_zero():
            return 
        P_N = P.get_P_N()
        if P_N.is_zero(): return None
        return self.LM_LC(P_N)

    def is_LM_in_P_I(self, P:IntegralPolynomial) ->  bool:
        LM_P, _ = self.LM_LC(P)
        P_I = P.get_P_I()
        if P_I.is_zero(): return False
        LM_P_I, _ = self.LM_LC(P_I)
        return LM_P_I == LM_P
    
    def is_LM_in_P_N(self, P:IntegralPolynomial) ->  bool:
        LM_P, _ = self.LM_LC(P)
        P_N = P.get_P_N()
        if P_N.is_zero(): return False
        LM_P_N, _ = self.LM_LC(P_N)
        return LM_P_N == LM_P
        
    def display_rules(self, sys):
        display(Math(r"\{")) 
        for eq in sys:
            LM, LC = self.LM_LC(eq)
            key = IntegralPolynomial({LM:LC})
            value = self.polynomials_subtraction(eq, key)
            value = self.product_P_Coeff(value,-1)
            arrow = r"{\Huge \color{red} \mathbf{\rightarrow}}"  
            key_repr = key.repr_display_math()
            value_repr = value.repr_display_math()
            export = Math(f"{key_repr} {arrow} {value_repr}") 
            display(export)
        display(Math(r"\}"))

    def display_rules_without_coeff(self, sys):
        display(Math(r"\{")) 
        for eq in sys:
            LM, LC = self.LM_LC(eq)
            key = IntegralPolynomial({LM:1})
            value = eq.get_content_as_dict()
            del value[LM]
            for k,v in value.items():
                value[k]=1
            value=IntegralPolynomial(value)
            # value = self.product_P_Coeff(value,-1)
            arrow = r"{\Huge \color{red} \mathbf{\rightarrow}}"  
            key_repr = key.repr_display_math()
            value_repr = value.repr_display_math()
            export = Math(f"{key_repr} {arrow} {value_repr}") 
            display(export)
            print(self.parameters)
            print([expr_has_symbol(eq.get_integral_repr(),s) for s in self.parameters])
    
        display(Math(r"\}"))
         
    def display_LMs(self, sys):
        display(Math(r"\{")) 
        for eq in sys:
            LM, LC = self.LM_LC(eq)
            key = IntegralPolynomial({LM:LC})
            arrow = r"{\Huge \color{red} \mathbf{\rightarrow}}"  
            key_repr = key.repr_display_math()
            export = Math(f"{key_repr} {arrow} ...") 
            display(export)
        display(Math(r"\}"))
         

    def normalize_LC_of_P(self, 
                        P: IntegralPolynomial,
                        simplify_coeff=True) -> IntegralPolynomial:
        _, LC = self.LM_LC(P)
        normalized_P = {}
        for M, coeff in P.get_content(): 
            normalized_P[M] = coeff/LC
        P_norm = IntegralPolynomial(normalized_P, simplify_coeff=simplify_coeff)
        return P_norm, LC
    
    def monomials_product(self, 
                          M: IM, 
                          N: IM,
                          simplify_coeff=True)-> IntegralPolynomial:
        e = M.get_nb_int()
        f = N.get_nb_int()
        m0n0 = M.get_content()[0]*N.get_content()[0]
        if e == f == 0:
            MN = {IM(m0n0):1}
        elif e == 0 and f != 0:
            N1p = N.cut("1+").get_content() #N1plus
            MN  = {IM(m0n0,*N1p):1} 
        elif e != 0 and f== 0 :
            M1p = M.cut("1+").get_content() #N1plus
            MN = {IM(m0n0,*M1p): 1}
        else:
            N1p = N.cut("1+").get_content() #N1plus
            M1p = M.cut("1+").get_content() #N1plus
            sh = ShuffleList(M1p,N1p)
            mons_dict = {}
            for elem in sh:
                mons = IM(m0n0,*elem)
                if mons not in mons_dict:
                    mons_dict[mons] =1
                else:
                    mons_dict[mons] += 1 
            MN = mons_dict
        return IntegralPolynomial(MN,simplify_coeff=simplify_coeff)

    def fusion(self, M,N):
        """
        M = IM(x(t))
        N = IM(1,y(t),z(t)) 
        order = [x(t),y(t),z]
        return IM(x(t),y(t),z(t)) 
        """
        L1 = M.get_content()
        L2 = N.get_content()
        res = [L1[0]*L2[0]]
        i, j = 1, 1
        while i!=len(L1) and j!=len(L2): 
            #L1_i <= L2_j
            if self.IMO_le(IM(L1[i]), IM(L2[j])): 
                res += [L1[i]]
                i += 1
            else:
                res += [L2[j]]
                j += 1
        if i<len(L1):
            res += [*L1[i:]]
        else:
            res += [*L2[j:]]

        res = IM(*res) 
        assert res == self.LM_LC(self.monomials_product(M,N))[0]
        return res

    def anti_fusion(self,M,N):
        """
        find an integral monomial N2 such that lm(N \cdot N2) = M
        retrun 1 if N=M
        """
        if N.get_nb_int() > M.get_nb_int():
            return None
        if not self.IMO_le(N,M):
            return None
        M_c = M.get_content()
        N_c = N.get_content()
        if M_c[0] == N_c[0] == 1:
            N2_0 = 1
        else:
            q, r = sp.div(M_c[0],N_c[0])
            if r != 0: return None
            N2_0 = q 
        diff = diff_lists(M_c[1:],N_c[1:])
        N2 = IM(*[N2_0, *diff])
        #now that we have a candidate for N2, we need to 
        #check that lm(N \cdot N2) = M
        N_dot_N2 = self.monomials_product(N,N2)
        LM_N_dot_N2, _ = self.LM_LC(N_dot_N2)
        if LM_N_dot_N2 == M:
            return N2
        else:
            return None 
    
    def product_P_Coeff(self, 
                        P: {IntegralPolynomial, dict}, 
                        alpha: sp.Expr,
                        simplify_coeff=True,
                        return_dict=False) -> {IntegralPolynomial, dict}:
        """
        alpha is cst 
        """
        if type(P) == dict:
            alpha_P = dict_mul_by_coeff(P, alpha)
        elif type(P) == IntegralPolynomial:
            alpha_P = dict_mul_by_coeff(P.get_content_as_dict(), alpha)
        else:
            raise ValueError
        if return_dict:
            return alpha_P
        return IntegralPolynomial(alpha_P,simplify_coeff=simplify_coeff)

    def polynomials_add(self, 
                        P: {IntegralPolynomial, dict}, 
                        Q: {IntegralPolynomial, dict},
                        simplify_coeff=True,
                        return_dict=False) -> {IntegralPolynomial, dict}: 
        if type(P) == dict and type(Q) == dict:
            L = [P,Q]
        elif type(P) == IntegralPolynomial and type(Q) == IntegralPolynomial:
            L = [P.get_content_as_dict(), Q.get_content_as_dict()]
        else:
            raise ValueError
        PplusQ = dicts_addition(L)
        if return_dict:
            return PplusQ
        return IntegralPolynomial(PplusQ,simplify_coeff=simplify_coeff)
    
    def polynomials_subtraction(self, 
                                P: IntegralPolynomial, 
                                Q: IntegralPolynomial,
                                simplify_coeff=True,
                                return_dict=False) -> {IntegralPolynomial, dict}: 
        if type(P)==dict and type(Q)==dict:
            L = [P,Q]
        elif type(P)==IntegralPolynomial and type(Q)==IntegralPolynomial:
            L = [P.get_content_as_dict(), Q.get_content_as_dict()]
        else:
            raise ValueError
        PminusQ = dicts_subtraction(L)
        if return_dict:
            return PminusQ
        return IntegralPolynomial(PminusQ,simplify_coeff=simplify_coeff)
    

    def polynomials_product(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial,
                            simplify_coeff=True) -> IntegralPolynomial: 
        PQ = IntegralPolynomial(0)
        for M_P, c_P in P.get_content():
            for M_Q, c_Q in Q.get_content(): 
                M_PdotM_Q = self.monomials_product(
                                M_P,
                                M_Q,
                                simplify_coeff=simplify_coeff
                            )
                c_P_c_Q_M_PdotM_Q = self.product_P_Coeff(
                                        M_PdotM_Q,
                                        c_P*c_Q,
                                        simplify_coeff=simplify_coeff
                            )
                PQ = self.polynomials_add(PQ, 
                                          c_P_c_Q_M_PdotM_Q,
                                        simplify_coeff=simplify_coeff
                            )
        return PQ 
    
    def integrate_monomial(self, M: IM):
        return IM(1,*M.get_content())

    def integrate_polynomial(self, 
                             P: IntegralPolynomial,
                             simplify_coeff=False) -> IntegralPolynomial:
        Int_P = {}
        for M, coeff in P.get_content():
            Int_M = self.integrate_monomial(M)
            Int_P[Int_M] = coeff
        return IntegralPolynomial(Int_P,simplify_coeff=simplify_coeff)
 
    def add_prefix_to_polynomial(self, 
                                prefix: IM, 
                                P: IntegralPolynomial) -> IntegralPolynomial:
        new_P = {} 
        for M, coeff in P.get_content():
            pref_M = M.add_prefix(prefix)
            new_P[pref_M] = coeff
        return IntegralPolynomial(new_P)

    def reduced_product(self, 
                        P:IntegralPolynomial, 
                        M:IM,
                        simplify_coeff=True) -> IntegralPolynomial:
        """
        see section 3.1   
        assert M[0] = 1 and |M| > 0 and lm(P)=lm(P_I) and P_I != 0 
        reduced_product = (P \cdot M) - \int (M]1+] \cdot P)
        """   
        assert (M.cut("0") == IM(1) and M.get_nb_int() > 0)

        LM_P,_ = self.LM_LC(P)
        P_I = P.get_P_I()
        assert not P_I .is_zero()
        LM_P_I,_ = self.LM_LC(P_I)
        assert LM_P == LM_P_I 
        M1p = IntegralPolynomial(M.cut("1+"),simplify_coeff=simplify_coeff)
        M = IntegralPolynomial(M,simplify_coeff=simplify_coeff)
        #(P \cdot M)
        PdotM = self.polynomials_product(P,M,simplify_coeff=simplify_coeff) 
        
        #\int (M]1+] \cdot P)
        IntMdotP = self.integrate_polynomial(
                        self.polynomials_product(M1p,P,simplify_coeff=simplify_coeff),
                        simplify_coeff=simplify_coeff
                    ) 

        reduced_product = self.polynomials_add(
                            PdotM ,self.product_P_Coeff(IntMdotP, -1,simplify_coeff=simplify_coeff),
                            simplify_coeff=simplify_coeff
                        )
        return reduced_product
        
    def polynomial_power(self, 
                        P:IntegralPolynomial,
                        n:int,
                        simplify_coeff=True) -> IntegralPolynomial:
        assert is_int(n) 
        assert isinstance(P,IntegralPolynomial)
        if n == 0: return IntegralPolynomial(IM(1))
        P_pow_n = P
        for _ in range(n-1):
            P_pow_n = self.polynomials_product(
                        P_pow_n,
                        P,
                        simplify_coeff=simplify_coeff
            )
        return P_pow_n
    
    def reduced_power(self, 
                      P:IntegralPolynomial, 
                      n:int,
                      simplify_coeff=True) -> IntegralPolynomial:
        """
        see section 3.2  

        P^{\circled{n}} = n (\int (P_I[cut{1+}] cdot P_N^{n-1})) + P_N^n
        """
        assert is_int(n) and n >= 1 
        if n==1: return P
        P_I = P.get_P_I()
        P_N = P.get_P_N() 
        P_I_1plus = P_I.cut_P("1+") 
        P_N_pow_n_minus_one = self.polynomial_power(
                        P_N, 
                        n-1,
                        simplify_coeff=simplify_coeff
        )

        P_N_pow_n = self.polynomials_product(
            P_N_pow_n_minus_one, 
            P_N,
            simplify_coeff=simplify_coeff
        )

        #lets compute n (\int (P_I[cut{1+}] cdot P_N^{n-1})) in temp
        temp = self.integrate_polynomial(
                    self.polynomials_product(
                        P_I_1plus, 
                        P_N_pow_n_minus_one,
                        simplify_coeff=simplify_coeff
                     ),
                simplify_coeff=simplify_coeff
            )

        temp = self.product_P_Coeff(temp, n, simplify_coeff=simplify_coeff)

        reduced_power = self.polynomials_add(
                    temp, 
                    P_N_pow_n,
                    simplify_coeff=simplify_coeff
            )

        return reduced_power
    
    def reduction_M_by_P_simple_case(self,
                                    M: IM, 
                                    P: IntegralPolynomial
                                    ) -> IntegralPolynomial:
        return reduction_M_by_P_simple_case(self, M, P)
    
    def reduction_M_by_P_reduced_power(self,
                                       M: IM, 
                                       P: IntegralPolynomial
                                       ) -> IntegralPolynomial:
        return reduction_M_by_P_reduced_power(self, M, P)
    
    def reduction_M_by_P(self,
                         M: IM, 
                         P: IntegralPolynomial
                        ) -> IntegralPolynomial:
        return reduction_M_by_P(self,M,P)
    
    def reduce(self, 
                Q: IntegralPolynomial, 
                T: OrderedSet[IntegralPolynomial]
            ) -> IntegralPolynomial:
        return reduce(self,Q,T)
    
    def auto_reduce(self,  
                    T:OrderedSet[IntegralPolynomial]
                ) -> OrderedSet[IntegralPolynomial]:
        return auto_reduce(self,T)
    
    def critical_pairs_PI_QI(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PI_QI(self,P,Q)
    
    def critical_pairs_PI_QN(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PI_QN(self,P,Q)
    
    def critical_pairs_PN_QN(self,
                            P: IntegralPolynomial,
                            Q: IntegralPolynomial) -> IntegralPolynomial:
        return critical_pairs_PN_QN(self,P,Q)
    
    def critical_pairs(self,
                       R: OrderedSet[IntegralPolynomial]
                    ) -> OrderedSet [IntegralPolynomial]:
        return critical_pairs(self,R)
    
    def find_A_A0_G_F(self, 
                      P:IntegralPolynomial
                      ) -> tuple[IntegralPolynomial]:
        return find_A_A0_G_F(self,P)
    
    def update_exp(self, 
                T_prime: OrderedSet[IntegralPolynomial],
                E: OrderedSet[sp.Function, sp.Function, IntegralPolynomial]
                ) -> tuple:
        return update_exp(self,T_prime,E)
         
    def extend_X_with_exp_and_log(self,
                      E: set[sp.Function, sp.Function, IntegralPolynomial],
                      L: OrderedSet[sp.Function, IntegralPolynomial]
                      ) -> list:
        return extend_X_with_exp_and_log(self, E,L)

    def update_log(self, 
                T_prime: OrderedSet[IntegralPolynomial],
                L: OrderedSet[sp.Function, IntegralPolynomial]
                ) -> tuple:
        return update_log(self,T_prime,L)
    
    def integral_elimination(self,
                            F: OrderedSet[IntegralPolynomial],
                            disable_exp: bool = False,
                            disable_log: bool = False,
                            disable_critical_pairs: bool = False,
                            nb_iter: int = 0) -> tuple:
        return integral_elimination(self, 
                                F, 
                                disable_exp=disable_exp,
                                disable_log=disable_log,
                                disable_critical_pairs=disable_critical_pairs,
                                nb_iter=nb_iter)