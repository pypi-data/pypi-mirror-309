"""
███████████████████████████ofuscation_tools of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import lr,processing_tools
class oo:
    def __init__(self):
        self.pt = processing_tools()
        self.lr = lr
    def rotate_list(self,listInput:list, places_to_rotate:int):
        if not listInput:
            return listInput
        ll = len(listInput)
        if places_to_rotate >= ll:
            l_init = places_to_rotate - ll*int(places_to_rotate/ll)
        else:
            l_init = places_to_rotate
        rslt = []
        for i in range(ll):
            x = i + l_init
            if x >= ll:
                x-= ll
            rslt.append(listInput[x])
        return rslt
    def ep(self,strInput:str,initiator:int=0)->str:
        odir = self.pt.dictstr_to_dict(self.pt.decrypt(self.lr,'Z1quEwrfhRu2R0VtpiyLTnXIEX5-cimK4VUKtStDUk8='))
        w = []
        for i in range(len(strInput)):
            w.append(strInput[i])
        exceptionList = [i for i in odir["r"] if i in odir["l"]]
        a = odir["r"]
        b = self.rotate_list(odir["l"],places_to_rotate=initiator)
        for i in range(len(w)):
            c = w[i]
            if c in a and c not in exceptionList:
                w[i] = b[a.index(c)]
            elif c in b and c not in exceptionList:
                w[i] = a[b.index(c)]
        rslt = ''
        for i in w:
            rslt += i
        del odir
        del w
        del a
        del b
        del c
        return rslt