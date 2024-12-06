
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from textwrap import fill
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import os
import xlsxwriter
def plot_mudlog(file,dept_column,gas_chromatographs,description,descr_depth,descr_text,oilshow,oilshow_depth,oilshow_text,lithology,lithology_top,lithology_bottom,lithology_type,utiliy_path):
    
    
    fig = plt.figure(figsize=(15, 190))  # Increase the figure size to fit the third row
    c = np.arange(0,300000,50)
    gs = gridspec.GridSpec(3, 6, figure=fig, height_ratios=[0.2, 8, 0.2], width_ratios=[1, 0.5, 0.5, 3, 0.5, 2])
    axs = []
    for i in range(18):
        row = i // 6  
        col = i % 6   
        ax = fig.add_subplot(gs[row, col])  
        ax.set_xticks([])
        axs.append(ax)
        if i != 6:
            axs[i].set_yticks([])        
    maxs = c[file[dept_column].max()>c][-1]+150
    mins = c[file[dept_column].min()<=c][0]-150
    
    description[descr_depth] = pd.to_numeric(description[descr_depth].astype("string").str.replace(',', ''))
    
    axs[9].scatter(np.ones(len(description)),description[0],color="white")
    axs[9].set_ylim([maxs, mins])
    
    for i in range(len(description)):
        wrapped_text = fill("  "+description.loc[i,descr_text], width=60)  # Adjust width as needed
        axs[9].annotate(wrapped_text.replace("\n","\n  ") ,(1,description.loc[i,descr_depth]), ha="left", wrap=True,fontsize=9)
    axs[9].set_xlim([1,200])

    fig.delaxes(axs[7])
    plt.subplots_adjust(wspace=0, hspace=0)
    
    axs[0].text(0.20,0.5,"CORRELATION",fontweight='bold')
    axs[1].text(0.3,0.3,"Depth Labels", rotation=270,fontweight='bold')
    axs[2].text(0.3,0.5,"Interp\nLith",fontweight='bold')
    axs[3].text(0.3,0.5,"Lithology Descriptions",fontweight='bold')
    axs[4].text(0.3,0.4,"Oil Show", rotation=270,fontweight='bold')
    axs[-6].text(0.23,0.5,"CORRELATION",fontweight='bold')
    axs[-5].text(0.3,0.3,"Depth Labels", rotation=270,fontweight='bold')
    axs[-4].text(0.3,0.5,"Interp\nLith",fontweight='bold')
    axs[-3].text(0.3,0.5,"Lithology Descriptions",fontweight='bold')
    axs[-2].text(0.3,0.4,"Oil Show", rotation=270,fontweight='bold')
    
    img = plt.imread(utiliy_path+"\\1.PNG")
    axs[-1].imshow(img, extent=[-5, 80, -5, 30],aspect="auto")
    axs[8].set_ylim([maxs, mins])
    axs[8].set_xlim([0,1])
    for j in range(len(lithology[lithology_top])):
        a = float("".join(str(lithology[lithology_top][j]).split(",")))
        b = float("".join(str(lithology[lithology_bottom][j]).split(",")))
        c = [a,b]
        d = lithology[lithology_type][j]
    
        if "shale" in d.lower():
            axs[8].fill_betweenx(c,0,1,facecolor="white",hatch="--")
            s=1
        elif "siltstone" in d.lower():
            axs[8].fill_betweenx(c,0,1,facecolor=tuple(np.array([255,126,0])/255),hatch="...",step="pre")
        elif "sandstone" in d.lower():
            axs[8].fill_betweenx(c,0,1,facecolor=tuple(np.array([255,242,0])/255),hatch="...")
        elif "dolomite" in d.lower():
            axs[8].fill_betweenx(c,0,1,facecolor=tuple(np.array([87,38,120])/255),hatch="-/-/-/")
        elif "limestone" in d.lower():
            axs[8].fill_betweenx(c,0,1,facecolor=tuple(np.array([153,217,234])/255),hatch="-/-/-/-/")
            
        
    axs[6].step(file["ROP"], file[dept_column], where='pre', color='black', linewidth=2)  # 'mid' aligns steps to the middle
    axs[6].set_xlim([0,5])
    
    axs[10].fill_betweenx(oilshow[oilshow_depth],  0, oilshow[oilshow_text]+0.5,color="black", step='pre')
    axs[10].tick_params(top=True, labeltop=True, bottom=True, labelbottom=True)
    axs[10].set_xticks([0,1,2,3,4])
    axs[10].set_xticklabels([0,"VSSO","SS0","SO","GS"],rotation=90,fontsize=6)
    axs[10].set_xlim([0.5,4.5])
    
    for i in np.arange(0,5,1):
        axs[10].axvline(i, color='black', linewidth=0.2)
        
    img = plt.imread(utiliy_path+"\\1.PNG")
    axs[5].imshow(img, extent=[-5, 80, -5, 30],aspect="auto")
    axs[5].set_xticks([])
    
    c = []
    plot = ["TG","C1","C2","C3","C4","C5"]
    colors = ["red","blue",tuple(np.array([192,80,70])/255),tuple(np.array([85,187,67])/255),tuple(np.array([204,204,0])/255),"darkturquoise"]
    style = ["solid","solid","--","dashdot","dotted","solid"]
    c = pd.DataFrame({"colors":colors,"style":style},index=plot)
    
    plotneed = c.loc[gas_chromatographs].reset_index()["index"]
    plotcolor = c.loc[gas_chromatographs].reset_index()["colors"] 
    plotstyle= c.loc[gas_chromatographs].reset_index()["style"]
    for i,j,k in zip(plotneed,plotcolor,plotstyle):
        axs[11].plot(file[i],file[dept_column],color=j,linewidth=2, linestyle=k)
        axs[11].set_xlim([0,150])
        s = file[[dept_column,i]]
        s = s[s[i]>150]
        s[i] = s[i]-150
        d = s.reset_index()["index"].values
        dd = pd.DataFrame(index=np.arange(1,len(file)),columns=[i])
        dd[i]= -1
        dd[dept_column] = file[dept_column]
        dd.loc[d,i] = s[i]
        ax2 = axs[11].twiny()
        ax2.plot(dd[i],dd[dept_column],color=j,linewidth=2, linestyle=k)
        ax2.fill_betweenx(dd[dept_column],  0, dd[i],facecolor=j,alpha=0.1,hatch="//")
        ax2.set_xticks([])
        ax2.set_xlim([0,150])
        
    
    
    axs[11].set_xlim([0,150])
    nos = [0,1,2,3,4,5,7,8,9,11,12,13,14,15,16,17]
    for i in nos:
        axs[i].set_xticks([])
    
    axs[10].set_yticks([])
    axs[11].set_yticks([])
    
    for y in np.arange(mins, maxs, 100):

   
        axs[6].annotate("0",(0.25,y+2),color="black",fontsize=6,fontweight="bold")
        axs[6].annotate("ROP (min/ft)",(1.5,y+2),color="black",fontsize=6,fontweight="bold")
        axs[6].annotate("5",(4.5,y+2),color="black",fontsize=6,fontweight="bold")
    
        axs[11].annotate("0",(5,y+1.5),color="red",fontsize=6,fontweight="bold")
        axs[11].annotate("TG (units)",(65,y+1.5),color="red",fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+1.5),color="red",fontsize=6,fontweight="bold")
    
    
        axs[11].annotate("0",(5,y+3.5),color="blue",fontsize=6,fontweight="bold")
        axs[11].annotate("C1 (units)",(65,y+3.5),color="blue",fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+3.5),color="blue",fontsize=6,fontweight="bold")
    
    
        axs[11].annotate("0",(5,y+5.5),color=tuple(np.array([192,80,70])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("C2 (units)",(65,y+5.5),color=tuple(np.array([192,80,70])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+5.5),color=tuple(np.array([192,80,70])/255),fontsize=6,fontweight="bold")
        
    
        axs[11].annotate("0",(5,y+7.5),color=tuple(np.array([85,187,67])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("C3 (units)",(65,y+7.5),color=tuple(np.array([85,187,67])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+7.5),color=tuple(np.array([85,187,67])/255),fontsize=6,fontweight="bold")
    
    
        axs[11].annotate("0",(5,y+9.5),color=tuple(np.array([204,204,0])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("C4 (units)",(65,y+9.5),color=tuple(np.array([204,204,0])/255),fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+9.5),color=tuple(np.array([204,204,0])/255),fontsize=6,fontweight="bold")
    
        axs[11].annotate("0",(5,y+11.5),color="darkturquoise",fontsize=6,fontweight="bold")
        axs[11].annotate("C5 (units)",(65,y+11.5),color="darkturquoise",fontsize=6,fontweight="bold")
        axs[11].annotate("150",(140,y+11.5),color="darkturquoise",fontsize=6,fontweight="bold")
    
    for ax in [axs[6],axs[10],axs[11]]:
        ax.set_ylim([maxs, mins])
        ax.set_yticks(np.arange(mins,maxs,10))
    
        ax.minorticks_on()
        for y in np.arange(mins, maxs, 50):
            ax.axhline(y=y, color='black', linewidth=2.5)
        for y in np.arange(mins, maxs, 10):
            ax.axhline(y=y, color='black', linewidth=1.5)
        for y in np.arange(mins, maxs, 2):
            ax.axhline(y=y, color='black', linewidth=0.5)
    
    axs[6].yaxis.tick_right()
    
    axs[10].set_yticks([])
    axs[11].set_yticks([])
    
        
    for label in axs[6].get_yticklabels():
        y_val = float(label.get_text())
       
        if y_val % 50 == 0:  # Every 50 ft
            label.set_fontweight('bold')  # Make label bold
            label.set_fontsize(10)  # Optionally adjust font size
        else:
            label.set_fontweight('normal')
            label.set_fontsize(8)     
    for i in np.arange(15,150,15):
        axs[11].axvline(i, color='gray', linewidth=0.01)
    for i in np.arange(0.5,5,0.5):
        axs[6].axvline(i, color='gray', linewidth=0.01)
    plt.savefig(r"F:\Plot_Design\PLOTB.pdf",format="pdf",bbox_inches='tight')
    
    plt.show()
    return fig

def header_mudlog(df_well_headers,utiliy_path,type,header_location):
    if type=="auto":
        global well,LOC,STATE,CTRY,API,SPD,BMC,GE,LITO,LFROM,FORM,DRILLFLUIDS,RIG,AFENUMBER,FIELD,DRILLINGCOMPLETED,TD,OA,CY,SRVC,GNAME,GEA,CNTY
        try:
            well = df_well_headers[df_well_headers["Mnemonic"]=="WELL"]["Value"].values[0]
        except:
            well = ""
        try:
            LOC = df_well_headers[df_well_headers["Mnemonic"]=="LOC"]["Value"].values[0]
        except:
            LOC = ""
        try:
            STATE = df_well_headers[df_well_headers["Mnemonic"]=="STAT"]["Value"].values[0]
        except:
            STATE = ""
        try:
            CTRY = df_well_headers[df_well_headers["Mnemonic"]=="CTRY"]["Value"].values[0]
        except:
            CTRY = ""
        
        try:
            API = df_well_headers[df_well_headers["Mnemonic"]=="API"]["Value"].values[0]
        except:
            API = ""
            
        try:
            SPD = df_well_headers[df_well_headers["Mnemonic"]=="SPUDDATE"]["Value"].values[0]
        except:
            SPD  = ""
            
        try:
            BMC = df_well_headers[df_well_headers["Mnemonic"]=="BOTTOMHOLECOORDINATES"]["Value"].values[0]
        except:
            BMC  = ""
        
        
        
        try:
            GE  = df_well_headers[df_well_headers["Mnemonic"]=="GROUNDELEVATION"]["Value"].values[0]
        except:
            GE  = ""
        
        try:
            LITO  = df_well_headers[df_well_headers["Mnemonic"]=="LOGGEDINTERVALTO"]["Value"].values[0]
        except:
            LITO  = ""
        
        try:
            LFROM  = df_well_headers[df_well_headers["Mnemonic"]=="LOGGEDINTERVALFROM"]["Value"].values[0]
        except:
            LFROM  = ""
        
        try:
            FORM  = df_well_headers[df_well_headers["Mnemonic"]=="FORMATION"]["Value"].values[0]
        except:
            FORM  = ""
        
        try:
            DRILLFLUIDS  = df_well_headers[df_well_headers["Mnemonic"]=="TYPEOFDRILLINGFLUID"]["Value"].values[0]
        except:
            DRILLFLUIDS  = ""
        
        try:
            CNTY  = df_well_headers[df_well_headers["Mnemonic"]=="CNTY"]["Value"].values[0]
        except:
            CNTY  = ""
        
        try:
            RIG = df_well_headers[df_well_headers["Mnemonic"]=="RIG"]["Value"].values[0]
        except:
            RIG = ""
        
        try:
            AFENUMBER = df_well_headers[df_well_headers["Mnemonic"]=="AFENUMBER"]["Value"].values[0]
        except:
            AFENUMBER = ""
        
        try:
            FIELD= df_well_headers[df_well_headers["Mnemonic"]=="FIELD"]["Value"].values[0]
        except:
            FIELD = ""
        
        try:
            DRILLINGCOMPLETED= df_well_headers[df_well_headers["Mnemonic"]=="DRILLINGCOMPLETED"]["Value"].values[0]
        except:
            DRILLINGCOMPLETED = ""
        
        try:
            TD= df_well_headers[df_well_headers["Mnemonic"]=="TOTALDEPTH"]["Value"].values[0]
        except:
            TD = ""
        
        try:
            OA= df_well_headers[df_well_headers["Mnemonic"]=="OPERATORADDRESS"]["Value"].values[0]
        except:
            OA = ""
        try:
            CY= df_well_headers[df_well_headers["Mnemonic"]=="COMP"]["Value"].values[0]
        except:
            CY = ""
        
        try:
            SRVC= df_well_headers[df_well_headers["Mnemonic"]=="SRVC"]["Value"].values[0]
        except:
            SRVC = ""
        
        try:
            GNAME= df_well_headers[df_well_headers["Mnemonic"]=="GEOLOGISTNAME"]["Value"].values[0]
        except:
            GNAME = ""
        
        try:
            GEA= df_well_headers[df_well_headers["Mnemonic"]=="GEOLOGISTADDRESS"]["Value"].values[0]
        except:
            GEA = ""

        try:
            GR= df_well_headers[df_well_headers["Mnemonic"]=="GEO"]["Value"].values[0]
        except:
            GR = ""


    elif type=="manual":

        if not os.path.exists(header_location+'\\header_format.xlsx'):
            workbook = xlsxwriter.Workbook(header_location+'\\header_format.xlsx')
     
            worksheet = workbook.add_worksheet()
            text = ["Well Name","Location","State","Country","API Number","Geographic Region","Spud Date","Surface Coordinates","Bottom Hole Coordinates","Ground Elevation","Logged Interval From","Logged Interval To","Formation","Type of Drilling Fluid"]
            text1 = ["County","Rig Number","APE #","Field","Drilling Completed","Total Depth","Geologist Name","Geologist Address","Service Company","Company Address","Operator Address"]
                
            print(len(text+text1))
            for j,i in enumerate(text):
                worksheet.write(f'A{j+1}', i)
    
            for j,i in enumerate(text):
                worksheet.write(f'B{j+1}', " ")
    
            for j,i in enumerate(text1):
                worksheet.write(f'A{j+15}', i)
    
            for j,i in enumerate(text1):
                worksheet.write(f'B{j+15}', " ")
    
        
            workbook.close()

        read = pd.read_excel(header_location+"\\header_format.xlsx",header=None)
        read = read.astype("str")
        print(read)
        well,LOC,STATE,CTRY,API,GR,SPD,BMC,BMC,GE,LFROM,LITO,FORM,DRILLFLUIDS,CNTY,RIG,AFENUMBER,FIELD,DRILLINGCOMPLETED,TD,GNAME,GEA,SRVC,CY,OA = read.loc[0][1],read.loc[1][1],read.loc[2][1],read.loc[3][1],read.loc[4][1],read.loc[5][1],read.loc[6][1],read.loc[7][1],read.loc[8][1],read.loc[9][1],read.loc[10][1],read.loc[11][1],read.loc[12][1],read.loc[13][1],read.loc[14][1],read.loc[15][1],read.loc[16][1],read.loc[17][1],read.loc[18][1],read.loc[19][1],read.loc[20][1],read.loc[21][1],read.loc[22][1],read.loc[23][1],read.loc[24][1]

    fig8 = plt.figure(figsize=(25, 45),frameon=False)
    gs1 = fig8.add_gridspec(nrows=21, ncols=6, left=0.05, right=0.48, wspace=1.2,hspace=73.3)
    print(well,LOC,STATE,CTRY,API,GR,SPD,BMC,BMC,GE,LFROM,LITO,FORM,DRILLFLUIDS,CY,RIG,AFENUMBER,FIELD,DRILLINGCOMPLETED,TD)
    def add_rounded_border(ax, linewidth=3, edgecolor='black', radius=0.02):
        # Get the bounding box of the subplot and create a rounded rectangle
        bbox = ax.get_position()
        rounded_box = FancyBboxPatch((bbox.x0, bbox.y0), bbox.width, bbox.height,
                                     boxstyle=f"round,pad=0.018,rounding_size={radius}",
                                     transform=fig8.transFigure, linewidth=linewidth,
                                     edgecolor=edgecolor, facecolor='none')
        fig8.patches.append(rounded_box)
    
    
    f8_ax1 = fig8.add_subplot(gs1[0:4, :])
    f8_ax2 = fig8.add_subplot(gs1[4:8, :])
    f8_ax3 = fig8.add_subplot(gs1[8:11, 0:3])
    f8_ax4 = fig8.add_subplot(gs1[8:11, 3:6])
    f8_ax5 = fig8.add_subplot(gs1[11:13, :])
    f8_ax6 = fig8.add_subplot(gs1[13:17, :])
    f8_ax7 = fig8.add_subplot(gs1[17:21, :])
    
    
    for ax in [f8_ax1, f8_ax2, f8_ax3, f8_ax4, f8_ax5, f8_ax6, f8_ax7]:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        add_rounded_border(ax)
    
    text = ["Well Name","Location","State","Country","API Number","Geographic Region","Spud Date","Surface Coordinates","Bottom Hole Coordinates","Ground Elevation","Logged Interval","Formation","Type of Drilling Fluid"]
    textinfo = [well,LOC,STATE,CTRY,API,GR,SPD,BMC,BMC,GE,LFROM + "   To   " + LITO ,FORM,DRILLFLUIDS]
    j=0.8
    for J,i in enumerate(text):
        f8_ax1.annotate(i,(0.2,j),color="black",fontsize=10,fontweight="bold",ha="right")
        f8_ax1.annotate(textinfo[J],(0.22,j),color="black",fontsize=10,ha="left")
        
        j=j-0.062
        
    text1 = ["County","Rig Number","APE #","Field","Drilling Completed","Total Depth"]
    text1info=[CNTY,RIG, AFENUMBER,FIELD,DRILLINGCOMPLETED,TD]
    
    j=0.8-(0.062)*2
    for J,i in enumerate(text1):
        f8_ax1.annotate(i,(0.65,j),color="black",fontsize=10,fontweight="bold",ha="right")
        f8_ax1.annotate(text1info[J],(0.67,j),color="black",fontsize=10,ha="left")
        
        j=j-0.062
    f8_ax1.annotate("Measured Depth Log",(0.4,0.95),color="black",fontsize=12,fontweight="bold")
    f8_ax2.imshow(plt.imread(utiliy_path+"\\2.png"),extent=[0,1,0,1],aspect="auto")
    
    f8_ax2.annotate("Company",(0.1,0.85),color="black",fontsize=12,fontweight="bold",ha="right")
    f8_ax2.annotate("Address",(0.1,0.75),color="black",fontsize=12,fontweight="bold",ha="right")
    try:
        wrapped_text1 = fill(OA, width=29) 
    except:
        wrapped_text1 = ""
    f8_ax2.annotate(CY,(0.12,0.85),color="black",fontsize=12,ha="left")
    f8_ax2.annotate(wrapped_text1,(0.12,0.75),color="black",fontsize=12,ha="left",va="center")
    
    f8_ax2.annotate("Operator",(0.45,0.95),color="black",fontsize=12,fontweight="bold")
    
    f8_ax3.imshow(plt.imread(utiliy_path+"\\3.png"),extent=[0,1,0,1],aspect="auto")
    
    f8_ax3.annotate("Geologist",(0.4,0.95),color="black",fontsize=12,fontweight="bold")
    f8_ax4.annotate("Color Coding",(0.4,0.95),color="black",fontsize=12,fontweight="bold")
    
    
    f8_ax3.annotate("Name",(0.20,0.75),color="black",fontsize=12,fontweight="bold",ha="right")
    f8_ax3.annotate("Company",(0.20,0.65),color="black",fontsize=12,fontweight="bold",ha="right")
    f8_ax3.annotate("Address",(0.20,0.55),color="black",fontsize=12,fontweight="bold",ha="right")
    
    f8_ax3.annotate(GNAME,(0.25,0.75),color="black",fontsize=12,ha="left",va="center")
    f8_ax3.annotate(SRVC,(0.25,0.65),color="black",fontsize=12,ha="left",va="center")
    try:
        wrapped_text2 = fill(GEA, width=29) 
    except:
        wrapped_text2 = ""
    f8_ax3.annotate(wrapped_text2,(0.25,0.55),color="black",fontsize=12,ha="left",va="center")
    
    f8_ax4.imshow(plt.imread(utiliy_path+"\\4.png"),extent=[0,1,0,1],aspect="auto")
    f8_ax5.annotate("ROCK TYPES",(0.35,0.70),color="black",fontweight="bold",fontsize=20,ha="left",va="center")
    
    f8_ax5.imshow(plt.imread(utiliy_path+"\\5.png"),extent=[0,1,0,1],aspect="auto")
    f8_ax6.imshow(plt.imread(utiliy_path+"\\6.png"),extent=[0,1,0,1],aspect="auto")
    f8_ax6.annotate("ACCESSORIES",(0.35,0.90),color="black",fontweight="bold",fontsize=20,ha="left",va="center")
    f8_ax6.annotate("Fossils",(0.022,0.80),color="black",fontweight="bold",fontsize=15,ha="left",va="center")
    f8_ax6.annotate("Minerals",(0.31,0.80),color="black",fontweight="bold",fontsize=15,ha="left",va="center")
    f8_ax6.annotate("Stringer",(0.64,0.80),color="black",fontweight="bold",fontsize=15,ha="left",va="center")
    f8_ax7.annotate("Other Symbols",(0.35,0.90),color="black",fontweight="bold",fontsize=20,ha="left",va="center")
    
    f8_ax7.annotate("Oil Show",(0.024,0.80),color="black",fontweight="bold",fontsize=10)
    f8_ax7.annotate("Porosity",(0.18,0.80),color="black",fontweight="bold",fontsize=10)
    f8_ax7.annotate("Engineering",(0.34,0.80),color="black",fontweight="bold",fontsize=10)
    f8_ax7.annotate("Rounding",(0.53,0.80),color="black",fontweight="bold",fontsize=10)
    f8_ax7.annotate("Textures",(0.66,0.80),color="black",fontweight="bold",fontsize=10)
    f8_ax7.annotate("Sorting",(0.805,0.80),color="black",fontweight="bold",fontsize=10)
    
    f8_ax7.imshow(plt.imread(utiliy_path+"\\7.png"),extent=[0,1,0,1],aspect="auto")
    
    return fig8


def generate_mudlog(figure2,figure,name_of_file):

    with PdfPages(name_of_file) as pdf:
        pdf.savefig(figure2, bbox_inches='tight', pad_inches=0)
        pdf.savefig(figure, bbox_inches='tight', pad_inches=0)  # Save the first figure
          # Save the second figure
    # Close the figures after saving to release memory
    plt.close(figure2)
    plt.close(figure)