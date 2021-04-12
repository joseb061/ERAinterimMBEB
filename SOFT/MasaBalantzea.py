import netCDF4 as nc
from matplotlib import pyplot as plt
import numpy as np
import math

def maskaragroen(): #bakarrik behin exekutatu mask.nc sortzeko. 
    
    #lehenengo datuetako jatorria deklaratu
    inc=nc.Dataset("interim2017.nc")
    inc2=nc.Dataset("fixed.nc")
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

    #--------------------------------- maskarako hasierako balioak
    oA[:,:]=np.zeros((nlat,nlon),"d")
    olx[:,:]=np.zeros((nlat,nlon),"d")
    oly[:,:]=np.zeros((nlat,nlon),"d")
    #--------------------------------------------------

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
    inGreenland=(themask>=0.05)
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
    onx[:,:]=np.zeros((nlat,nlon),'d')

    ony=onc.createVariable("ny",'d',("latitude","longitude"))
    ony.long_name="Bektore unitarioaren osagai meridionala"
    ony[:,:]=np.zeros((nlat,nlon),'d')

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
    print (AGROEN)
    return AGROEN
def eskalarraP(p,frakald,Atokiko,azal):
    emaitzaP= np.add.reduce(np.add.reduce(p*frakald*Atokiko)) 
    return emaitzaP
def eskalarraR(r,frakald,Atokiko,azal):
    emaitzaR= (np.add.reduce(np.add.reduce(r*Atokiko*frakald))) 
    return emaitzaR
def eskalarraE(e,frakald,Atokiko,azal):
    emaitzaE= np.add.reduce(np.add.reduce(-e*frakald*Atokiko)) 
    return emaitzaE
def eskalarraQ(qx,qy,nx,ny,lx,ly,frakald,azal):
    emaitzaq= np.add.reduce(np.add.reduce((qx*nx*ly+qy*ny*lx)))
    #emaitzaq= np.add.reduce(np.add.reduce((qx+qy)*frakald))
    return emaitzaq
def eskalarraW(w1,w2,frakald,Atokiko,azal): #positivo - negtivo
    emaitza= (np.add.reduce(np.add.reduce((w1-w2)*frakald*Atokiko)))/(2.*2.628e+6) # /segundu egiteko   
    return emaitza
def urteBat(urtea):

    
    print ("-------------------------------------------------------------------------------------\n")
    print (urtea,"\n")

    
    
    inc3=nc.Dataset('mask.nc','r',format="NETCDF3_CLASSIC")

    frak= np.array(inc3.variables["frakzioa"][:,:],'d')
    Azaleratoki= np.array(inc3.variables["Azalera"][:,:],'d') #tokian tokiko azalera
    NX=np.array(inc3.variables["nx"][:,:],'d')
    NY=np.array(inc3.variables["ny"][:,:],'d')
    LX=np.array(inc3.variables["lx"][:,:],'d')
    LY=np.array(inc3.variables["ly"][:,:],'d')
    A= azaleraGroenlandian(frak,Azaleratoki)  # groenladia osoko azalera
    
    

    inc4=nc.Dataset('interim%d.nc'%(urtea,),"r",format="NETCDF3_CLASSIC")
    
    
    
    E=np.zeros(24,"d")
    P=np.zeros(24,"d")
    R=np.zeros(24,"d")
    Q=np.zeros(12,"d")
    n=np.zeros(12,"d")
    Wderibatua=np.zeros(12,"d")
    Eunit=np.zeros(24,"d")
    Punit=np.zeros(24,"d")
    Runit=np.zeros(24,"d")
   
    Ever=np.zeros(6,"d")
    Pver=np.zeros(6,"d")
    Rver=np.zeros(6,"d")
    Eunitver=np.zeros(6,"d")
    Punitver=np.zeros(6,"d")
    Runitver=np.zeros(6,"d")
    
    

    
    #------------------------------------------- PREZIPIT. + EVAPORAZIOA+ RUNOFF 

    itime=inc4.variables["time"]
    itimestr=itime.units
    
    for i in range(24): #24 hilabete guztiak #verano 11-16              
        prezipit= np.array(inc4.variables["tp"][i,:,:],'d') #[i,:,:]     
        evapor= np.array(inc4.variables["e"][i,:,:],'d')  
        runoff= np.array(inc4.variables["ro"][i,:,:],'d')      
        E[i]= eskalarraE(evapor,frak,Azaleratoki,A) #m/eguna
        P[i]= eskalarraP(prezipit,frak,Azaleratoki,A) 
        R[i]=eskalarraR(runoff,frak,Azaleratoki,A)
        #orain dimensioak aldatu m/egun-etik kg/s-ra
        Eunit[i]= E[i]*(1000./86400.) #kg/s
        Punit[i]= P[i]*(1000./86400.) #kg/s
        Runit[i]= R[i]*(1000./86400.) #kg/s
   
    #print "Urte osoko ebaporazioa=", np.sum(Eunit)*(3.154e+7/(1.e+12)),"Gt/urte" #urte bat= 3,154e+7s
    #print "Urte osoko prezipitazioa=", np.sum(Punit)*(3.154e+7/(1.e+12)),"Gt/urte" #urte bat= 3,154e+7s  
    #print "Urte osoko batazbesteko prezipitazioa =", np.mean(Punit)*(3.154e+7/(1.e+12)),"Gt/urte" #urte bat= 3,154e+7s 
    #print "Urte osoko batazbesteko ebaporazioa=", np.mean(Eunit)*((3.154e+7)/1.e+12),"Gt/urte"
    #print "Urte osoko batazbesteko runoff=", np.mean(Runit)*((3.154e+7)/1.e+12), "Gt/urte"
    
    #-------------------------------------------------------------- EPR verano
    for i in range(6): #24 hilabete guztiak              
        i=+11
        prezipit= np.array(inc4.variables["tp"][i,:,:],'d') #[i,:,:]     
        evapor= np.array(inc4.variables["e"][i,:,:],'d')  
        runoff= np.array(inc4.variables["ro"][i,:,:],'d')      
        Ever[i-11]= eskalarraE(evapor,frak,Azaleratoki,A) #m/eguna
        Pver[i-11]= eskalarraP(prezipit,frak,Azaleratoki,A) 
        Rver[i-11]=eskalarraR(runoff,frak,Azaleratoki,A)
        #orain dimensioak aldatu m/egun-etik kg/urte-ra
        Eunitver[i-11]= Ever[i-11]*(1000.*365.) #kg/urte
        Punitver[i-11]= Pver[i-11]*(1000.*365.) #kg/urte
        Runitver[i-11]= Rver[i-11]*(1000.*365.) #kg/urte
        

    Pmeanver=np.mean(Punitver)/1.e+12
    Emeanver= np.mean(Eunitver)/1.e+12
    Rmeanver= np.mean(Runitver)/1.e+12
    Smeanver= Pmeanver-Emeanver-Rmeanver

    itime=inc4.variables["time"]
    itimestr=itime.units
    thedate=nc.num2date(itime[11],itimestr)
    afile= open("/home/joseba/Escritorio/programa_tfg_mayo/mass_Verano.txt","a") #udako P,E,R,S batezbestekoak [Gt/urte]-tan.
    afile.write("%d %g %g %g %g\n"%(thedate.year,Pmeanver,Emeanver,Rmeanver,Smeanver))
    afile.close()



   

    #----------------------------------------------------------------------------------- watervapor Q
    inc5=nc.Dataset('atmosferico%d.nc'%(urtea,),"r",format="NETCDF3_CLASSIC")
    inc6=nc.Dataset('atmosferico%d.nc'%(urtea-1,),"r",format="NETCDF3_CLASSIC")
    inc7=nc.Dataset('atmosferico%d.nc'%(urtea+1,),"r",format="NETCDF3_CLASSIC")
    
    for i in range(12):
        fluxeast = np.array(inc5.variables["p71.162"][i,:,:],'d')
        fluxnorth= np.array(inc5.variables["p72.162"][i,:,:],'d')
        Q[i]= eskalarraQ(fluxeast,fluxnorth,NX,NY,LX,LY,frak,A) #kg/s
        
   
    print ("Urte osoko VAPOR FLUX Q kg/y:", np.sum(Q)*3.154e+7/(1.e+12))
    print ("Urte osoko  mean VAPOR FLUX Q kg/y:", np.mean(Q)*3.154e+7/(1.e+12),"\n")
 

    
    #-------------------------------------------------------------------------------------  W deribatua
    
    a=np.array(inc6.variables["tcwv"][11,:,:],'d')
    b=np.array(inc5.variables["tcwv"][1,:,:],'d')
    c=np.array(inc5.variables["tcwv"][10,:,:],'d')
    d=np.array(inc7.variables["tcwv"][0,:,:],'d')
   
    Wderibatua[0]= eskalarraW(b,a,frak,Azaleratoki,A)  #mugalde baldintzak definitu. 
    Wderibatua[11]=eskalarraW(d,c,frak,Azaleratoki,A) 
    
    for i in range(10):  
        
        tini= i+1
        tplus= tini+1
        tminus= tini-1                    
        watervapor=np.array(inc5.variables["tcwv"][tplus,:,:],'d')
        watervaporb=np.array(inc5.variables["tcwv"][tminus,:,:],'d')
        Wderibatua[tini] = eskalarraW(watervapor,watervaporb,frak,Azaleratoki,A) # ENERO-FEBREO , ..., DICIEMBRE-NOVIEMBRE 
    
    print ("Urte osoko  mean VAPOR COLUMN W GT/y:", np.mean(Wderibatua)*3.154e+7/(1.e+12))

    #---------------------------------------------------------------------------------------------
    Pmean= np.mean(Punit)*(3.154e+7/(1.e+12)) # [Gt/urte]
    Emean= np.mean(Eunit)*((3.154e+7)/1.e+12)
    Rmean= np.mean(Runit)*((3.154e+7)/1.e+12)
    Qmean= np.mean(Q)*3.154e+7/(1.e+12)
    Wmean= np.mean(Wderibatua)*3.154e+7/(1.e+12)
    nmean= Emean-Pmean-Qmean-Wmean
    Smean= Pmean - Emean - Rmean

    print ("urte osoko cumulative Smean:", Smean)

    itime=inc4.variables["time"]
    itimestr=itime.units
    thedate=nc.num2date(itime[11],itimestr)
    afile= open("/home/joseba/Escritorio/programa_tfg_mayo/mass_storage.txt","a") #urtez urteko aldagaien batezbestekoak [Gt/urte]-tan
    afile.write("%d %g %g %g %g %g %g %g %g\n"%(thedate.year,Pmean,Emean,Rmean,Smean,Qmean,Wmean,nmean,Emean-Pmean)) 
    afile.close()

    for i in range (24):
        thedate=nc.num2date(itime[i],itimestr)
        rfile= open("/home/joseba/Escritorio/programa_tfg_mayo/EPR_hilabeteka.txt","a") # E, P ,R eta E-P hilabeteka [Gt/urte]-tan
        rfile.write("%d %d %g %g %g %g\n"%(thedate.year,thedate.month,Eunit[i]*(3.154e+7)/1.e+12,
        Punit[i]*(3.154e+7)/1.e+12,Runit[i]*(3.154e+7)/1.e+12,(Eunit[i]-Punit[i])*(3.154e+7)/1.e+12))
        #AURREKO DATUAK Gt/urte- tan grabatu dira.
   
    

    for i in range(12): 
        thedate=nc.num2date(itime[i],itimestr)  
        ofile= open("/home/joseba/Escritorio/programa_tfg_mayo/QW_hilabeteka.txt","a") # divQ eta dW/dt hilabeteka [Gt/urte]-tan
        ofile.write("%d %d %g %g\n"%(thedate.year,thedate.month,Q[i]*(3.154e+7)/1.e+12,Wderibatua[i]*(3.154e+7)
        /1.e+12))
    
    
    ofile.close()
    rfile.close()





#------------------------------------------------------------------------------------------
#                                  PROGRAMA NAGUSIA                           
#------------------------------------------------------------------------------------------
maskaragroen()
for urtea in range (1980,2018): # masa balantzerako (dW/dt erabiltzen ez den balantzerako) 1980-2019 periodoa erabili.
    urteBat(urtea)

