#include <wx/filename.h>
#include <wx/colour.h>
#include <wx/image.h>
#include <string>
#include "chatbot.h"
#include "chatlogic.h"
#include "chatgui.h"

// size of chatbot window
const int width = 414;
const int height = 736;

// wxWidgets APP
IMPLEMENT_APP(ChatBotApp);

std::string dataPath = "../";
std::string imgBasePath = dataPath + "images/";

bool ChatBotApp::OnInit()
{
    // create window with name and show it
    ChatBotFrame *chatBotFrame = new ChatBotFrame(wxT("Udacity ChatBot"));
    chatBotFrame->Show(true);

    return true;
}

// wxWidgets FRAME
ChatBotFrame::ChatBotFrame(const wxString &title) : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(width, height))
{
    // create panel with background image
    ChatBotFrameImagePanel *ctrlPanel = new ChatBotFrameImagePanel(this);

    // create controls and assign them to control panel
    _panelDialog = new ChatBotPanelDialog(ctrlPanel, wxID_ANY);

    // create text control for user input
    int idTextXtrl = 1;
    _userTextCtrl = new wxTextCtrl(ctrlPanel, idTextXtrl, "", wxDefaultPosition, wxSize(width, 50), wxTE_PROCESS_ENTER, wxDefaultValidator, wxTextCtrlNameStr);
    Connect(idTextXtrl, wxEVT_TEXT_ENTER, wxCommandEventHandler(ChatBotFrame::OnEnter));

    // create vertical sizer for panel alignment and add panels
    wxBoxSizer *vertBoxSizer = new wxBoxSizer(wxVERTICAL);
    vertBoxSizer->AddSpacer(90);
    vertBoxSizer->Add(_panelDialog, 6, wxEXPAND | wxALL, 0);
    vertBoxSizer->Add(_userTextCtrl, 1, wxEXPAND | wxALL, 5);
    ctrlPanel->SetSizer(vertBoxSizer);

    // position window in screen center
    this->Centre();
}

void ChatBotFrame::OnEnter(wxCommandEvent &WXUNUSED(event))
{
    // retrieve text from text control
    wxString userText = _userTextCtrl->GetLineText(0);

    // add new user text to dialog
    _panelDialog->AddDialogItem(userText, true);

    // delete text in text control
    _userTextCtrl->Clear();

    // send user text to chatbot 
     _panelDialog->GetChatLogicHandle()->SendMessageToChatbot(std::string(userText.mb_str()));
}

BEGIN_EVENT_TABLE(ChatBotFrameImagePanel, wxPanel)
EVT_PAINT(ChatBotFrameImagePanel::paintEvent) // catch paint events
END_EVENT_TABLE()

ChatBotFrameImagePanel::ChatBotFrameImagePanel(wxFrame *parent) : wxPanel(parent)
{
}

void ChatBotFrameImagePanel::paintEvent(wxPaintEvent &evt)
{
    wxPaintDC dc(this);
    render(dc);
}

void ChatBotFrameImagePanel::paintNow()
{
    wxClientDC dc(this);
    render(dc);
}

void ChatBotFrameImagePanel::render(wxDC &dc)
{
    // load backgroud image from file
    wxString imgFile = imgBasePath + "sf_bridge.jpg";
    wxImage image;
    image.LoadFile(imgFile);

    // rescale image to fit window dimensions
    wxSize sz = this->GetSize();
    wxImage imgSmall = image.Rescale(sz.GetWidth(), sz.GetHeight(), wxIMAGE_QUALITY_HIGH);
    _image = wxBitmap(imgSmall);
    
    dc.DrawBitmap(_image, 0, 0, false);
}

BEGIN_EVENT_TABLE(ChatBotPanelDialog, wxPanel)
EVT_PAINT(ChatBotPanelDialog::paintEvent) // catch paint events
END_EVENT_TABLE()

ChatBotPanelDialog::ChatBotPanelDialog(wxWindow *parent, wxWindowID id)
    : wxScrolledWindow(parent, id)
{
    // sizer will take care of determining the needed scroll size
    _dialogSizer = new wxBoxSizer(wxVERTICAL);
    this->SetSizer(_dialogSizer);

    // allow for PNG images to be handled
    wxInitAllImageHandlers();

    //// STUDENT CODE
    ////

    // create chat logic instance
    _chatLogic = new ChatLogic(); 

    // pass pointer to chatbot dialog so answers can be displayed in GUI
    _chatLogic->SetPanelDialogHandle(this);

    // load answer graph from file
    _chatLogic->LoadAnswerGraphFromFile(dataPath + "src/answergraph.txt");

    ////
    //// EOF STUDENT CODE
}

ChatBotPanelDialog::~ChatBotPanelDialog()
{
    //// STUDENT CODE
    ////

    delete _chatLogic;

    ////
    //// EOF STUDENT CODE
}

void ChatBotPanelDialog::AddDialogItem(wxString text, bool isFromUser)
{
    // add a single dialog element to the sizer
    ChatBotPanelDialogItem *item = new ChatBotPanelDialogItem(this, text, isFromUser);
    _dialogSizer->Add(item, 0, wxALL | (isFromUser == true ? wxALIGN_LEFT : wxALIGN_RIGHT), 8);
    _dialogSizer->Layout();

    // make scrollbar show up
    this->FitInside(); // ask the sizer about the needed size
    this->SetScrollRate(5, 5);
    this->Layout();

    // scroll to bottom to show newest element
    int dx, dy;
    this->GetScrollPixelsPerUnit(&dx, &dy);
    int sy = dy * this->GetScrollLines(wxVERTICAL);
    this->DoScroll(0, sy);
}

void ChatBotPanelDialog::PrintChatbotResponse(std::string response)
{
    // convert string into wxString and add dialog element
    wxString botText(response.c_str(), wxConvUTF8);
    AddDialogItem(botText, false);
}

void ChatBotPanelDialog::paintEvent(wxPaintEvent &evt)
{
    wxPaintDC dc(this);
    render(dc);
}

void ChatBotPanelDialog::paintNow()
{
    wxClientDC dc(this);
    render(dc);
}

void ChatBotPanelDialog::render(wxDC &dc)
{
    wxImage image;
    image.LoadFile(imgBasePath + "sf_bridge_inner.jpg");

    wxSize sz = this->GetSize();
    wxImage imgSmall = image.Rescale(sz.GetWidth(), sz.GetHeight(), wxIMAGE_QUALITY_HIGH);

    _image = wxBitmap(imgSmall);
    dc.DrawBitmap(_image, 0, 0, false);
}

ChatBotPanelDialogItem::ChatBotPanelDialogItem(wxPanel *parent, wxString text, bool isFromUser)
    : wxPanel(parent, -1, wxPoint(-1, -1), wxSize(-1, -1), wxBORDER_NONE)
{
    // retrieve image from chatbot
    wxBitmap *bitmap = isFromUser == true ? nullptr : ((ChatBotPanelDialog*)parent)->GetChatLogicHandle()->GetImageFromChatbot(); 

    // create image and text
    _chatBotImg = new wxStaticBitmap(this, wxID_ANY, (isFromUser ? wxBitmap(imgBasePath + "user.png", wxBITMAP_TYPE_PNG) : *bitmap), wxPoint(-1, -1), wxSize(-1, -1));
    _chatBotTxt = new wxStaticText(this, wxID_ANY, text, wxPoint(-1, -1), wxSize(150, -1), wxALIGN_CENTRE | wxBORDER_NONE);
    _chatBotTxt->SetForegroundColour(isFromUser == true ? wxColor(*wxBLACK) : wxColor(*wxWHITE));

    // create sizer and add elements
    wxBoxSizer *horzBoxSizer = new wxBoxSizer(wxHORIZONTAL);
    horzBoxSizer->Add(_chatBotTxt, 8, wxEXPAND | wxALL, 1);
    horzBoxSizer->Add(_chatBotImg, 2, wxEXPAND | wxALL, 1);
    this->SetSizer(horzBoxSizer);

    // wrap text after 150 pixels
    _chatBotTxt->Wrap(150);

    // set background color
    this->SetBackgroundColour((isFromUser == true ? wxT("YELLOW") : wxT("BLUE")));
}
