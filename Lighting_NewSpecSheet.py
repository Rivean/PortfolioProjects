from fpdf import FPDF
import pandas as pd
import math

# Read in data from syndication
data = pd.read_excel(r"C:\Users\arivera\OneDrive - craftmade.com\Desktop\Spec Sheet Data Exports\16032SB4_Specs.xlsx")

for row in data.itertuples(index=False):

    class PDF(FPDF):
        def header(self):
            # logo
            self.image('Craftmade_Logo_Black.png', 10, 15, 80)
        
        # Page Footer
        def footer(self):
            # Set position of footer
            self.set_y(-15)
            # Set font
            self.set_font('helvetica', 'I', 12)
            # Text for the footer
            self.cell(0, 10, "Craftmade.com | 1-800-486-4892" , align= "C")

    # Create PDF object
    pdf = PDF('P', 'mm', 'Letter')

    # Add a page
    pdf.add_page()

    # Add the main image of the item
    model_number = str(row[0])
    pdf.image(name = f'{model_number}.jpg', x=10, y=35, w=110) # y should be 30 default w= 125
    #pdf.image(name = f'{model_number}.jpg', x=20, y=30, h=80) # Most Sconces and hanging fixtures

    # Display the model number
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_xy(x= 100, y= 15)
    pdf.cell(w= 100, h= 5, txt= model_number, align='R', border=False)

    # Diplay the item description
    pdf.set_font('helvetica', '', 16)
    pdf.set_xy(x= 100, y=26)
    pdf.cell(w= 100, h=5, txt= row[1], align='R', border=False )
   

    # Diplay the item finish
    pdf.set_font('helvetica', '', 13)
    pdf.set_xy(x= 100, y= 32)
    pdf.cell(w=100, h=5, txt= row[2], align= 'R', border=False)

    # Display the item UPC
    pdf.set_font('helvetica', '', 11)
    pdf.set_xy(x= 100, y= 38)
    pdf.cell(w=100, h=5, txt= f"UPC#{int(row[3])}", align='R', border=False)

    # Additional Finishes Section
    pdf.set_xy(x=150, y=55) #x is 140 originally y 65
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(255,255,255)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w=50, h=8, txt= 'Additional Finishes', fill=True, border=False)

    pdf.set_xy(x=150,y=63.5) #y 73.5
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_text_color(0,0,0)
    #pdf.multi_cell(w=35, h=4, txt=f"{row[39]}\n{row[40]}\n{row[41]}", border=False) # Starts at row 39, adjust based on how many finishes

    # Create Measurements section
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(255,255,255)
    pdf.set_xy(x=10, y= 120)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w= 50, h= 8,txt='Measurements', fill=True, border=False)

    pdf.set_xy(x= 10,y=128)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(w=40, h=4, txt= 'Length (in):\nWidth (in):\nHeight (in):\nExtension (in):\nDownrod/Chain Length (in):\nLeadwire (in):\nProduct Weight (lbs):\n\
Carton Length (in):\nCarton Width (in):\nCarton Height (in):\nCarton Cube:\nCarton Weight (lbs):\nOversize:', border=False)

    # Create the variables for the Measurement values
    length = row[4]
    if math.isnan(length):
        length = 'N/A'
    else:
        length = row[4]
    width = row[5]
    height = row[6]
    extension = row[7]
    if math.isnan(extension):
        extension = 'N/A'
    else:
        extension = row[7]
    downrod_chain_length = row[8]
    if type(downrod_chain_length) is str:
        downrod_chain_length = row[8]
    elif math.isnan(downrod_chain_length):
        downrod_chain_length = 'N/A'
    lead_wire = row[9]
    if math.isnan(lead_wire):
        lead_wire = 'N/A'
    product_weight = row[10]
    carton_length = row[11]
    carton_width = row[12]
    carton_height = row[13]
    carton_cube = row[14]
    carton_weight = row[15]
    oversize = row[16]

    pdf.set_xy(x=45, y= 128)
    pdf.multi_cell(w=15, h=4, txt=f'{length}\n{width}\n{height}\n{extension}\n{downrod_chain_length}\n{lead_wire}\n{product_weight}\n{carton_length}\n{carton_width}\n\
    {carton_height}\n{carton_cube}\n{carton_weight}\n{oversize}', align= 'R', border=False)

    # Create Fixture section
    pdf.set_xy(x=70, y= 120)
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(255,255,255)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w= 55, h=8, txt='Fixture', fill=True, border=False)

    pdf.set_xy(x=70, y= 128)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(w=35,h=4, txt=f'Mounting Method:\nMounting Location:\nBody Material:\nUp/Down Mount:', border=False)

    # Create variables for Fixture section
    mounting_method = row[17]
    mounting_location = row[18]
    body_material = row[19]
    up_down_mount = row[20]
    if type(up_down_mount) is str:
        up_down_mount = row[20]
    elif math.isnan(up_down_mount):
        up_down_mount = 'N/A'
  

    pdf.set_xy(x= 90, y=128)
    pdf.multi_cell(w=35, h= 4, txt=f'{mounting_method}\n{mounting_location}\n{body_material}\n{up_down_mount}', align='R', border=False)

    # Create Electrical/Lighting section
    pdf.set_xy(x= 135,y= 120)
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(255,255,255)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w= 65, h=8, txt= 'Electrical/Lighting', fill=True, border=False)

    # Create variables for the fields
    light_source_type = row[21]
    if type(light_source_type) is str:
        light_source_type = row[21]
    elif math.isnan(light_source_type):
        light_source_type = 'N/A'

    number_of_bulbs = row[22]
    bulbs_included = row[23]
    total_lighting_watts = row[24]
    if type(total_lighting_watts) is str:
        total_lighting_watts = row[24]
    elif math.isnan(total_lighting_watts):
        total_lighting_watts = 'N/A'

    socket_type = row[25]
    dimmable = row[26]
    if type(dimmable) is str:
        dimmable = row[26]
    elif math.isnan(dimmable):
        dimmable = 'N/A'

    delivered_lumens = row[27]
    if math.isnan(delivered_lumens):
        delivered_lumens = 'N/A'
    else:
        delivered_lumens = row[27]
    cri = row[28]
    if math.isnan(cri):
        cri = 'N/A'
    else:
        cri = row[28]
    cct = row[29]
    if type(cct) is str:
        cct = row[29]
    elif math.isnan(cct):
        cct = 'N/A'
    shade_finish_material = row[30]
    if type(shade_finish_material) is str:
        shade_finish_material = (row[30] + ' ' + row[31])
    elif math.isnan(shade_finish_material):
        shade_finish_material = 'N/A'
    shade_width = row[32]
    if math.isnan(shade_width):
        shade_width = 'N/A'
    else:
        shade_width = row[32]
    shade_height = row[33]
    if math.isnan(shade_height):
        shade_height = 'N/A'
    else:
        shade_height = row[33]

    # field labels
    pdf.set_xy(x=135, y= 128)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(w= 45, h=4, txt= f'Light Source Type:\nNumber of Bulbs:\nBulbs Included:\nTotal Wattage:\nSocket Type:\nDimmable\n\
Delivered Lumens:\nCRI:\nColor Temp:\nShade Finish/Material:\nShade Width (in):\nShade Height (in):', border=False)

    pdf.set_xy(x= 163, y= 128)
    pdf.multi_cell(w=37,h=4, txt= f"{light_source_type}\n{number_of_bulbs}\n{bulbs_included}\n{total_lighting_watts}\n{socket_type}\n{dimmable}\n\
    {delivered_lumens}\n{cri}\n{cct}\n{shade_finish_material}\n{shade_width}\n{shade_height}", align="R", border=False)

    # Create Certifications section
    pdf.set_xy(x=70, y= 150)
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(255,255,255)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w= 55, h=8, txt='Certifications', fill=True, border=False)

    # Add field names
    pdf.set_xy(x=70, y= 158)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.multi_cell(w=35, h=4, txt= f"Safety Rating:\nTitle 20:\nTitle 24 (JA8):\nADA:",border=False)

    # Create variables for the values
    safety_rating = row[34]
    if type(safety_rating) is str:
        safety_rating = row[34]
    elif math.isnan(safety_rating):
        safety_rating = 'N/A'
    title_20 = row[35]
    if type(title_20) is str:
        title_20 = row[35]
    elif math.isnan(title_20):
        title_20 = 'N/A'
    title_24 = row[36]
    if type(title_24) is str:
        title_24 = row[36]
    elif math.isnan(title_24):
        title_24 = 'N/A'
    ada = row[37]
    if type(ada)is str:
        ada = row[37]
    elif math.isnan(ada):
        ada = 'N/A'
   
    pdf.set_xy(x=85, y=158)
    pdf.multi_cell(w=40, h=4, txt= f'{safety_rating}\n{title_20}\n{title_24}\n{ada}', align="R", border=False)

    # Create Warranty section
    pdf.set_xy(x=70, y= 180)
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(255,255,255)
    pdf.set_fill_color(90,90,90)
    pdf.cell(w= 55, h=8, txt='Warranty', fill=True, border=False)

    warranty = row[38]

    pdf.set_xy(x=70, y= 188)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.cell(w=55, h=5, txt= warranty, border=False)

    # Section for additional notes IE Slope with SMA only etc; Comment out if not needed
    '''
    pdf.set_xy(x=10, y= 215)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(0,0,0)
    pdf.cell(w= 55, h=8, txt='*Includes Removable Decorative Strap', border=False)
    #'''


    # Output the PDF 
    pdf.output(f'{model_number}_SpecSheet.pdf')