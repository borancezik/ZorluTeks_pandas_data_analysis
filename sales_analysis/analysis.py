import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce
import datetime



#veri setleri import edilir
df1 = pd.read_csv("data/MAGAZADETAY0912.csv")
df2 = pd.read_csv("data/ZorluFaturalar2802_V2.csv",nrows=100000)
df3 = pd.read_csv("data/ZorluData2020_0107_VW_ZTMTERIAL.csv",nrows=1000)


#gereksiz kolonlar belirlernir
drop1 = ["OPEN","PROMO"]

drop = ["Mağaza Müdürü","Bölge Sorumlusu","Enlem","Boylam","Faks","Kapanış Tarihi",
       "Telefon","E-Posta","Adres","Adres Kodu","Regüle","Açılış Tarihi","Ülke",'CITYCODE1', 'CITYCODE2']

drop2 = ['ZK1', 'ZK2', 'ZK3', 'ZTMMARKA', 'ZTMATLGR1', 'ZTMATLGR2', 'ZTMATLGR3',
       'ZTMATLGR4', 'ZSISLEY', 'ZTTK1', 'ZTTK2', 'ZTTK3', 'ZTTK4', 'ZTTK5',
       'ZTTMARKA', 'TZTMATLGR1', 'TZTMATLGR2', 'TZTMATLGR3', 'TZTMATLGR4','ZMATL_GRP','ZTMTL_TYP',"TXTMD"]


#gereksiz kolonlar veri setlerinde çıkartılır
df1.drop(drop , axis = 1, inplace = True)
df2.drop(drop1,axis =1, inplace = True)
df3.drop(drop2,axis = 1, inplace =True)


#işlenecek kolonların isimlerini değiştirdim
df1.rename(columns={"Hesap No":"Hesap_No"}, inplace = True)
df2.rename(columns={"ZTCSTMR2":"Hesap_No","BILL_NUM":"FaturaNo","CALMONTH":"FATURAYILAY","ZTMTERIAL":"UrunKodu","DATE":"Tarih"}, inplace=True)
df3.rename(columns={"ZTMTERIAL":"UrunKodu"},inplace=True)

#Nan değerler cıkartıldı
df1.dropna(inplace=True)
df2.dropna(inplace=True)
df3.dropna(inplace=True)


df1.drop(df1.loc[df1['Hesap_No'] == 'YOK'].index,inplace=True)

df1['Hesap_No'] = df1['Hesap_No'].astype(int)
df2['Hesap_No'] = df2['Hesap_No'].astype(int)
df3['UrunKodu'] = df3['UrunKodu'].astype(int)


 

mrge = df1.merge(df2,how='inner',left_on='Hesap_No', right_on = 'Hesap_No')#left joın
#df_final = mrge.merge(df3,how='inner', left_on='UrunKodu', right_on='UrunKodu')#left joın#

#ilk 100000 bin satır için hangi magazaların toplam ne kadar satış yaptıgı ?
result1 = mrge[["Mağaza Adı","NETVAL_INV"]].groupby("Mağaza Adı").sum().sort_values("NETVAL_INV",ascending=False).head(15)

#ilk 100000 bin satır için hangi magazaların toplam kaç adet satış yaptıgı ?
result2 = mrge[["Mağaza Adı","NETVAL_INV"]].groupby("Mağaza Adı").count().sort_values("NETVAL_INV",ascending=False).head(15)

#mağazaların satış oranları
new_result = result1.merge(result2,left_index=True,right_index=True)
new_result["oran"] = new_result["NETVAL_INV_x"]/new_result["NETVAL_INV_y"]
print(new_result["oran"].sort_values(ascending=False))


#ilk 100000 bin satır için hangi illerin toplam kaç adet satış yaptıgı ?
result = mrge[["IL","NETVAL_INV"]].groupby("IL").count().reset_index().sort_values("NETVAL_INV",ascending=False).head(10)
sns.barplot(x="IL", y="NETVAL_INV",data=result)
plt.ylabel("SATIŞ ADETİ")
plt.xlabel("İL")
sns.light_palette("green")
plt.title("İLLERİN TOPLAM SATIŞ ADETLERİ")
plt.show()

#lk 100000 bin satır için hangi illerin toplam kaç tutar satış yaptıgı ?
result = mrge[["IL","NETVAL_INV"]].groupby("IL").sum().reset_index().sort_values("NETVAL_INV",ascending=False).head(10)
sns.barplot(x="IL", y="NETVAL_INV",data=result)
plt.ylabel("TOPLAM SATIŞ TUTARI")
plt.xlabel("İL")
sns.light_palette("green")
plt.title("İLLERİN TOPLAM SATIŞ TUTARLARI")
plt.show()


#Haftanın en çok hangi günleri satış olmuş
result = mrge[["DAYOFWEEK","FaturaNo"]].groupby("DAYOFWEEK").count().reset_index().sort_values("FaturaNo",ascending=False)
sns.barplot(x="DAYOFWEEK", y="FaturaNo",data=result)
plt.ylabel("SATIŞ ADETİ")
plt.xlabel("GÜNLER")
plt.title("HAFTALIK TOPLAM SATIŞ ADETLERİ")
plt.show()

#yılın hangi ayı satış olmuştur
result = mrge.groupby(["Bölge","IL"])["FaturaNo"].count()

mrge['Yıl'] = pd.DatetimeIndex(mrge['Tarih']).year
mrge['Ay'] = pd.DatetimeIndex(mrge['Tarih']).month

result = mrge[["Ay","FaturaNo"]].groupby("Ay").count().reset_index().sort_values("FaturaNo",ascending=False)
sns.barplot(x="Ay", y="FaturaNo",data=result)
plt.ylabel("SATIŞ ADETİ")
plt.xlabel("AYLAR")
plt.title("AYLIK TOPLAM SATIŞ ADETLERİ")
plt.show()




#İSTANBUL DİĞER BÖLGELERE GÖRE ÇOK FARK İÇERDİĞİ İÇİN ÇIKARTILIP KALAN İLLERE BAKILMISTIR/ adet

result = mrge[mrge["Bölge"]=="ANADOLU"]
result2 = result[["IL","FaturaNo"]].groupby("IL").count().reset_index().sort_values("FaturaNo",ascending=False).head(15)
sns.barplot(x="IL", y="FaturaNo",data=result2)
plt.ylabel("SATIŞ ADETİ")
plt.xlabel("İL")
plt.title("iLLERİN SATIŞ ADETİ(İSTANBUL HARİÇ)")
plt.show()


#İSTANBUL DİĞER BÖLGELERE GÖRE ÇOK FARK İÇERDİĞİ İÇİN ÇIKARTILIP KALAN İLLERE BAKILMISTIR/ tutar

result = mrge[mrge["Bölge"]=="ANADOLU"]
result2 = result[["IL","NETVAL_INV"]].groupby("IL").sum().reset_index().sort_values("NETVAL_INV",ascending=False).head(15)
sns.barplot(x="IL", y="NETVAL_INV",data=result2)
plt.ylabel("TOPLAM SATIŞ TUTARI")
plt.xlabel("İL")
plt.title("iLLERİN SATIŞ TUTARI(İSTANBUL HARİÇ)")
plt.show()


#İSTANBUL İLÇELERİNİN SATIŞ ADETLERİ
result = mrge[mrge["Bölge"]=="İSTANBUL"]
result2 = result[["İlçe","NETVAL_INV"]].groupby("İlçe").count().reset_index().sort_values("NETVAL_INV",ascending=False).head(15)
sns.barplot(x="İlçe", y="NETVAL_INV",data=result2)
plt.ylabel("SATIŞ ADETİ")
plt.xlabel("İL")
plt.title("İSTANBUL İLÇELERİN SATIŞ ADETLERİ")
plt.show()


"""mrge['oran'] = mrge['budget'] + mrge['actual']"""

#YERLEŞİM TÜRÜNE GÖRE SATIŞ ORANI
result1 = mrge[["Yerleşim Türü","NETVAL_INV"]].groupby("Yerleşim Türü").sum().sort_values("NETVAL_INV",ascending=False)
result2 =  mrge[["Yerleşim Türü","NETVAL_INV"]].groupby("Yerleşim Türü").count().sort_values("NETVAL_INV",ascending=False)

new_result = result1.merge(result2,left_index=True,right_index=True)
new_result["oran"] = new_result["NETVAL_INV_x"]/new_result["NETVAL_INV_y"]
new_result["Yerleşim Türü"] = new_result.index
sns.barplot(x="Yerleşim Türü", y="oran",data=new_result)
plt.title("YERLEŞİM TÜRÜNE GÖRE SATIŞ ORANI")
plt.ylabel("SATIŞ ORANI")
plt.xlabel("YERLEŞİM TÜRÜ")
plt.show()

#storeZorlu = storeZorlu[(storeZorlu['InvoiceDate']>='2019-01-01') & (storeZorlu['Quantity']>=0) & (storeZorlu['ZSMMDGR']>=0)  ] #storeZorlu['ZTCSTMR2']=='0010205759'


#YÜZ ÖLÇÜMÜNÜN SATIŞ ORANINA ETKİSİ
mrge.loc[mrge["Yüzölçümü (m2)"]<=250,"bucket"] = 'A.0-250 m2'
mrge.loc[(mrge["Yüzölçümü (m2)"]>250)&(mrge["Yüzölçümü (m2)"]<=400),"bucket"] = 'B.250-400 m2'
mrge.loc[(mrge["Yüzölçümü (m2)"]>400)&(mrge["Yüzölçümü (m2)"]<=650),"bucket"] = 'C.400-650 m2'
mrge.loc[mrge["Yüzölçümü (m2)"]>650,"bucket"] = 'D.650+ m2'

result1 = mrge[["bucket","NETVAL_INV"]].groupby("bucket").sum().sort_values("NETVAL_INV",ascending=False)
result2 =  mrge[["bucket","NETVAL_INV"]].groupby("bucket").count().sort_values("NETVAL_INV",ascending=False)

new_result = result1.merge(result2,left_index=True,right_index=True)
new_result["oran"] = new_result["NETVAL_INV_x"]/new_result["NETVAL_INV_y"]
new_result["bucket"] = new_result.index
sns.barplot(x="bucket", y="oran",data=new_result.sort_index(ascending=True))
plt.title("MAĞAZA BÜYÜKLÜĞÜNÜN SATIŞ ORANINA ETKİSİ")
plt.ylabel("SATIŞ ORANI")
plt.xlabel("YÜZÖLÇÜMÜ")
plt.show()


#yüz ölçümü ve perde alanı arasında olan oran
sns.scatterplot(x="Yüzölçümü (m2)",y="Perde Alanı (m2)", data=mrge, hue="Yerleşim Türü")
plt.title("YÜZÖLÇÜMÜ VE PERDE ALANI ARASINDA OLAN ORAN")
plt.show()

#print(mrge.info)

print(mrge)







