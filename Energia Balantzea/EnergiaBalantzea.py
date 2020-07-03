import netCDF4 as nc
from matplotlib import pyplot as plt
import numpy as np
import math


def maskaragroen(): #bakarrik behin exekutatu mask.nc sortzeko. 
    
    #lehenengo datuetako jatorria deklaratu
    inc=nc.Dataset("energia1982.nc")
    inc2=nc.Dataset("fixedenergy.nc")
    #------------------------------------------------------------------------------------------------------
   
    #orain nlon eta nlat lehenik eta behin luzeerak (.size-rekin) eta gero bektore bat sortu balio balio guztiekin. 
    nlon=inc.dimensions["longitude"].size
    lons=np.array(inc.variables["longitude"][:],'f')
    rlons=lons*np.pi/180. #radianetan jartzeko bektore osoa numpy-rekin [....]*pi/180  bektorearen karaktere guztiak biderkatzen ditu.
    nlat=inc.dimensions["latitude"].size #berdina latitudekin
    lats=np.array(inc.variables["latitude"][:],'f')
    rlats=lats*np.pi/180.

    print(nlon,nlat)  
    #-------------------------------------------------------------------------------------------

    #dimentsioak ligitudearentzat eta latitudearentzat eta hauek definitu ditugularik dimentsioak eta aldagaiak sortu gure mask.nc berriarrentzat  

    onc=nc.Dataset("mask.nc","w",format="NETCDF3_CLASSIC")  #fijatu w jarridugula idazteko
    onc.createDimension("longitude",nlon)
    onc.createDimension("latitude",nlat)


    olon=onc.createVariable("longitude",'f',("longitude",))
    olon.long_name=inc.variables["longitude"].long_name #jatorrizko fitxategiko izen berdina 
    olon.units=inc.variables["longitude"].units #jatorrizko unitate berdinak dituela adierzateko

    olat=onc.createVariable("latitude",'f',("latitude",))
    olat.long_name=inc.variables["latitude"].long_name
    olat.units=inc.variables["latitude"].units
    #------------------------------------------------------------------------------------------------------
    # Azalera eta lx eta ly definitzeko modu berean egin behar dugu baina orain dimentsioak arretik sortu ditugunez, soilik 
    # "Variables" definitu egin beharko ditugu 

    ILON=onc.createVariable("ILON",'f',("latitude","longitude"))
    ILAT=onc.createVariable("ILAT",'f',("latitude","longitude"))

    oA=onc.createVariable("Azalera",'d',("latitude","longitude"))
    oA.units="m**2"
    oA.long_name="Gelaxketako azalera"

    olx=onc.createVariable("lx",'d',("latitude","longitude"))
    olx.units="m"
    olx.long_name="Gelaxketako norabide zonaletako l bektoreen neurria"

    oly=onc.createVariable("ly",'d',("latitude","longitude"))
    oly.units="m"
    oly.long_name="Gelaxketako norabide meridionaleko l bektoreen neurria"
    #----------------------------------------------------------------------------------------------------------

    Rt=6371.0e3
    Rt2=Rt*Rt
    delta_lon=abs(rlons[1]-rlons[0])
    delta_lat=abs(rlats[1]-rlats[0])
    dlh=delta_lat/2.

    for ilon in range(nlon):
        for ilat in range(nlat):
            ILON[ilat,ilon]=ilon
            ILAT[ilat,ilon]=ilat
            oA[ilat,ilon]=Rt2*delta_lon*(math.sin(rlats[ilat]+dlh)-math.sin(rlats[ilat]-dlh))
            olx[ilat,ilon]=Rt*math.cos(rlats[ilat])*delta_lon
            oly[ilat,ilon]=Rt*delta_lat
            #oA[ilat,ilon]=olx[ilat,ilon]*oly[ilat,ilon]
            

    onc.sync()
    olon[:]=lons
    olat[:]=lats
    onc.sync()
    #----------------------------------------------------------------------------------------------------------
    # inc2 fitxerotik, autatu lsm
    # groenlandiatik kanpoko puntuak + not a number zenbakiak (GROEN-ren barruan) 0 balioa esleitu, bestetik lsm-n 0,1 edo andiagoak diren puntuak barruan

    themask=np.array(inc2.variables["lsm"][0,:,:],'d')
    inGreenland=(themask>=0.2)
    outGreenland=np.logical_not(inGreenland) #puntos erroneos
    gureGr=themask*inGreenland+0*outGreenland

    gureGr[85:nlat,0:103]=0.
    gureGr[69:nlat,217:nlon]=0.
    gureGr[45:nlat,0:77]=0.
    gureGr[0:nlat,0:25]=0.
    gureGr[0:25,0:35]=0.
    gureGr[280:nlat,0:49]=0.
    gureGr[111:nlat,0:nlon]=0.
    gureGr[41:nlat,269:nlon]=0.
    gureGr[0:20,0:50]=0.
    gureGr[0:24,0:45]=0.
    gureGr[0:10,0:60]=0.
    gureGr[0:16,40:60]=0.
    gureGr[0:14,40:70]=0.
    gureGr[0:14,54:72]=0.
    gureGr[0:15,54:72]=0.
    gureGr[0:12,54:78]=0.
    gureGr[0:17,0:56]=0.
    gureGr[0:16,0:62]=0.
    gureGr[0:15,0:72]=0.
    gureGr[0:18,0:54]=0.
    gureGr[0:17,0:57]=0.
    gureGr[0:16,0:63]=0.
    gureGr[0:13,0:72]=0.
    gureGr[0:12,48:79]=0.
    gureGr[0:12,0:78]=0.

    #--------------------------------------------------------------------------------------------------------------------
    omask=onc.createVariable("frakzioa",'d',("latitude","longitude"))
    omask.long_name="Gelaxkaren lur-frakzioa, 0...1"
    omask[:,:]=gureGr[:,:]

    onx=onc.createVariable("nx",'d',("latitude","longitude"))
    onx.long_name="Bektore unitarioaren osagai zonala"
    #onx[:,:]=np.zeros((nlat,nlon),'d')

    ony=onc.createVariable("ny",'f',("latitude","longitude"))
    ony.long_name="Bektore unitarioaren osagai meridionala"
    #ony[:,:]=np.zeros((nlat,nlon),'d')

for ilon in range(nlon):
        for ilat in range(nlat): 
            x=0.
            y=0.      
            if (omask[ilat,ilon]==0.):    # lehenik eta behin ikusi ea lurra den edo ez
                continue

            if (omask[ilat,ilon]>0.):   #  groenlandian dagoela ikusi dugularik lehenik eta behin puntu positiboak
                if (omask[ilat,ilon+1]==0.):
                    x=x+1.
                if (omask[ilat,ilon+1]>0.):
                    x=x+ 0.
                if (omask[ilat-1,ilon]==0.):
                    y= y+ 1.
                if (omask[ilat-1,ilon]>0.):
                    y=y+ 0.
                
                if (omask[ilat,ilon-1]==0.): #orain negatiboak
                    x=x-1.0
                if (omask[ilat,ilon-1]>0.):
                    x=x+0.
                if (omask[ilat+1,ilon]==0.):
                    y= y - 1.0
                if (omask[ilat+1,ilon]>0.):
                    y=y - 0.
            
            
            onx[ilat,ilon]= x 
            ony[ilat,ilon]= y
            #print "nx", onx[ilat,ilon]
            #print "ny", ony[ilat,ilon]
 
    #------------------------------------------------------------------------------------------------------------------
    onc.close()
    #Beste funtzioetan erabili ahal diren aldagaiak: frakzioa, nx, ny, lx, ly eta Azalera.
def azaleraGroenlandian(frakald,Azal): #groenlandiako azalera kalkulatzen du 
    AGROEN=np.add.reduce(np.add.reduce(frakald*Azal))
    
    return AGROEN
def eskalarraSW(sw,frakald,Atokiko,azal): #fluxu nebatiboak behera eta fluxu positiboak gora hartu. 
    emaitzasw= np.add.reduce(np.add.reduce(sw*Atokiko*frakald))*(1./86400.) 
    return emaitzasw
def eskalarraLW(lw,frakald,Atokiko,azal):
    emaitzalw= (np.add.reduce(np.add.reduce(lw*Atokiko*frakald)))*(1./86400.)
    return emaitzalw
def eskalarraLH(lh,frakald,Atokiko,azal):
    emaitzalh= (np.add.reduce(np.add.reduce(lh*Atokiko*frakald)))*(1./86400.) 
    return emaitzalh
def eskalarraSH(sh,frakald,Atokiko,azal):
    emaitzash= (np.add.reduce(np.add.reduce(sh*Atokiko*frakald)))*(1./86400.)
    return emaitzash
def urteBat(urtea):

    
    print "-------------------------------------------------------------------------------------"
    print ""
    print urtea
    print ""
    
    
    inc3=nc.Dataset("mask.nc")
    frak= np.array(inc3.variables["frakzioa"][:,:],'d')
    Azaleratoki= np.array(inc3.variables["Azalera"][:,:],'d') #tokian tokiko azalera
    NX=np.array(inc3.variables["nx"][:,:],'d')
    NY=np.array(inc3.variables["ny"][:,:],'d')
    LX=np.array(inc3.variables["lx"][:,:],'d')
    LY=np.array(inc3.variables["ly"][:,:],'d')
    A= azaleraGroenlandian(frak,Azaleratoki)  # groenladia osoko azalera
  
    

    inc4=nc.Dataset('energia%d.nc'%(urtea,))
    
    
    SW=np.zeros(24, "d")
    LW=np.zeros(24, "d")
    SH=np.zeros(24, "d")
    LH=np.zeros(24, "d")
    E=np.zeros(24, "d")
    sw=np.zeros(24, "d")
    lw=np.zeros(24, "d")
    sh=np.zeros(24, "d")
    lh=np.zeros(24, "d")
    tot= np.zeros(24, "d")

    #Negurako 

    ISW= np.zeros(5, "d")
    ILW= np.zeros(5, "d")
    ISH= np.zeros(5, "d")
    ILH= np.zeros(5, "d")
    IE= np.zeros(5, "d")
  
    #-------------------------------------------
    #------------------------------------------- SW LW SH LH 

    itime=inc4.variables["time"]
    itimestr=itime.units
    
    for i in range(24):                
       
        sortwave= np.array(inc4.variables["ssr"][i,:,:],'d') #[i,:,:]
        longwave= np.array(inc4.variables["str"][i,:,:],'d')  
        sensibleheat= np.array(inc4.variables["sshf"][i,:,:],'d')   
        latenteheat= np.array(inc4.variables["slhf"][i,:,:],'d')      
        
        SW[i]= eskalarraSW(sortwave,frak,Azaleratoki,A) 
        LW[i]= eskalarraLW(longwave,frak,Azaleratoki,A) 
        SH[i]=eskalarraSH(sensibleheat,frak,Azaleratoki,A)
        LH[i]=eskalarraLH(latenteheat,frak,Azaleratoki,A)
    

    
    
 
    

    #-----------------------------------------------------------------------------------
    #---------------------------------------------  FITXATEGIAN SARTU DATUAK
    for i in range(24): 
        thedate=nc.num2date(itime[i],itimestr) 
        tot[i]= (SW[i]+LW[i]+SH[i]+LH[i])/A
        sw[i]=SW[i]/A
        lw[i]=LW[i]/A
        sh[i]=SH[i]/A 
        lh[i]=LH[i]/A
       
        
        ofile= open("/home/joseba/Escritorio/programa_tfg_mayo/Energia_iterim/fitxategiak/todo.txt","a")
        ofile.write("%d %d %g %g %g %g %g\n"%(thedate.year,thedate.month,sw[i],lw[i],sh[i],lh[i],tot[i]))#Aldagaiak hilabetero [W/m**2]-tan
        
      
   
    ofile.close()
    #-------------------------------------------------------VERANO
    for i in range(7):
        thedate=nc.num2date(itime[i+10],itimestr)
        gfile= open("/home/joseba/Escritorio/programa_tfg_mayo/Energia_iterim/fitxategiak/Udako.txt","a")
        gfile.write("%d %d %g %g %g %g %g\n"%(thedate.year,thedate.month,sw[i+10],lw[i+10],sh[i+10],lh[i+10],tot[i+10]))#udako balioak [W/m**2]-tan
    
     
    #-----------------------------------------------------------INVIERNO
    

    thedate=nc.num2date(itime[i+10],itimestr)
    inc5= nc.Dataset('energia%d.nc'%(urtea-1,))
    sortwave_aurreko= np.array(inc5.variables["ssr"][23,:,:],'d') #[i,:,:]
    longwave_aurreko= np.array(inc5.variables["str"][23,:,:],'d')  
    sensibleheat_aurreko= np.array(inc5.variables["sshf"][23,:,:],'d')   
    latenteheat_aurreko= np.array(inc5.variables["slhf"][23,:,:],'d')      
    ISW[0]= eskalarraSW(sortwave_aurreko,frak,Azaleratoki,A)/A 
    ILW[0]= eskalarraLW(longwave_aurreko,frak,Azaleratoki,A)/A 
    ISH[0]=eskalarraSH(sensibleheat_aurreko,frak,Azaleratoki,A)/A
    ILH[0]=eskalarraLH(latenteheat_aurreko,frak,Azaleratoki,A)/A

    for i in range(4): 

        ISW[i+1]= sw[i]
        ILW[i+1]= lw[i]
        ISH[i+1]= sh[i]
        ILH[i+1]= lh[i]
    
    IE= ISW+ILW+ISH+ILH
    print "hau da neguko SW:", ISW
    
    for i in range(5): #invierno
        Nfile= open("/home/joseba/Escritorio/programa_tfg_mayo/Energia_iterim/fitxategiak/Neguko.txt","a")
        Nfile.write("%g %g %g %g %g\n"%(ISW[i],ILW[i],ISH[i],ILH[i],IE[i]))#neguko balioak [W/m**2]-tan
  
  
  
    gfile.close()
    Nfile.close()
    #------------------------------------------------   
    E= sw+lw+sh+lh
    print "short wave W/m**2", (np.mean(sw))
    print "long wave W/m**2",(np.mean(lw))
    print "sensible heat W/m**2", (np.mean(sh))
    print "latent heat W/m**2", (np.mean(lh))
    M= (E/(997.*334000.))*(1000.)*(3.154e+7/(1.e+12))
    Emean= np.mean(E)
    Eneto= np.sum(E)
    Mmean= np.mean(M)
    print "Batazbesteko Energia W/m**2:", (Emean)
    print "Energia netoa", Eneto



    
    
    thedate=nc.num2date(itime[11],itimestr)
    afile= open("/home/joseba/Escritorio/programa_tfg_mayo/Energia_iterim/fitxategiak/medias.txt","a")  
    afile.write("%d %g %g %g\n"%(thedate.year,Eneto,Emean,Mmean)) #batezbestko balioak [W/m**2]-tan
    afile.close()
    
    
#------------------------------------------------------------------------------------------
#                                  PROGRAMA PRINTZIPALA                            
#------------------------------------------------------------------------------------------

maskaragroen()
for urtea in range (1980,2018):  #bi urte falta dira 1979 eta 2019 
    urteBat(urtea)
    
