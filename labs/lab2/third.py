def mymax(iterable, key=lambda x: x):
    max_x = None
    max_key = None

    for i, x in enumerate(iterable):
        k = key(x)
        if i == 0 or k > max_key:
            max_x = x
            max_key = k

    return max_x



if __name__ == "__main__":
  maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
  maxchar = mymax("Suncana strana ulice")
  maxstring = mymax([
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"])

  maxlen = mymax([
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"], key=len)

  print(maxint)
  print(maxchar)
  print(maxstring)
  print(maxlen)

  D = {'burek':8, 'buhtla':5, 'slanic':4, 'kukuruzni':7}
  print(mymax(D,D.get))

  peeps = [('sinisa','segvic'),('marko','cupic'),('ivan','martinovic'),('iva','sovic')]
  print(mymax(peeps))

  D = {'a':3, 'b':4, 'c':12, 'e':1}
  print(mymax(D) + mymax(D,D.get))