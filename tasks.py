from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive





@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=0,
        )
    
    open_robot_order_website()
    orders = get_orders()

    """Navigate to Orders page"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()

    for order in orders:
        close_annoying_modal()
        order_number = fill_the_form(order)
        pdf_file = store_receipt_as_pdf(order_number)
        screenshot = screenshot_robot(order_number)
        embed_screenshot_to_receipt(screenshot, pdf_file)
        page.click("#order-another")
    
    archive_receipts()


        

def open_robot_order_website():
    """Navigate to the intranet then Login"""
    browser.goto("https://robotsparebinindustries.com/")
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")
    


def get_orders():
    """Download the orders file, read it as a table, and return the result"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    library = Tables()
    orders = library.read_table_from_csv(
    "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"])
    return orders


def close_annoying_modal():
    """Navigate to Orders page and close popup"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()
    page.click("text=Yep")


def fill_the_form(order):
    page = browser.page()
    """Input the Head value into the Dropdown select"""
    page.select_option("#head", str(order["Head"]))

    """Input the Body value into the Radio options"""
    CurrRadioOption = "#id-body-" + str(order["Body"])
    page.click(CurrRadioOption)

    """Input the Leg value into the Number box"""
    CurrInputOption = str(order["Legs"])
    page.locator("xpath=//label[contains(.,'3. Legs:')]/../input").fill(CurrInputOption)

    """Input the Address into the text box"""
    page.fill("#address", str(order["Address"]))

    """Preview the Robot and Select to order"""
    page.click("#preview")
    page.click("#order")

    """Mitigate the Intermitant Server Error"""
    while page.locator("#order").is_visible():
            page.click("#order")

    """retrieve order number from the receipt"""
    order_number = page.locator(".badge").text_content()
    return order_number


def store_receipt_as_pdf(order_number):
    page = browser.page()
    pdf = PDF()
    """Save the reciept HTML as PDF Text"""    
    pdf_file = ("output/order_receipt_" + order_number + ".pdf")
    pdf.html_to_pdf(page.locator("#order-completion").inner_html(), pdf_file)
    return pdf_file


def screenshot_robot(order_number):
    page = browser.page()
    """Take a screenshot of the robot preview and save it"""
    screenshot = ("output/order_screenshot_" + order_number + ".png")
    page.locator("#robot-preview-image").screenshot(path=screenshot)
    return screenshot
    

def embed_screenshot_to_receipt(screenshot, pdf_file):
    """Append the Robot preview screenshot to the reciept PDF"""
    list_of_files = [
        screenshot
        ]
    
    pdf = PDF()
    pdf.add_files_to_pdf(files=list_of_files, target_document=pdf_file, append=True)


def archive_receipts():
    """Create a Zip folder of all receipts"""
    lib = Archive()
    lib.archive_folder_with_zip('output', 'output/OrderReceipts.zip', include='*.pdf')

    





  





  
  



    





    
