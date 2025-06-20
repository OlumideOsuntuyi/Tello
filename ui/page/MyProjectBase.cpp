///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "MyProjectBase.h"

///////////////////////////////////////////////////////////////////////////

TelloGUI::TelloGUI( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* buttons;
	buttons = new wxBoxSizer( wxHORIZONTAL );

	wxBoxSizer* bSizer3;
	bSizer3 = new wxBoxSizer( wxVERTICAL );

	m_speed = new wxTextCtrl( this, wxID_ANY, _("Speed: 0x, 0y, 0z"), wxDefaultPosition, wxDefaultSize, 0 );
	m_speed->SetFont( wxFont( 12, wxFONTFAMILY_SCRIPT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, false, wxT("Comic Sans MS") ) );

	bSizer3->Add( m_speed, 0, wxALL|wxEXPAND, 5 );


	buttons->Add( bSizer3, 1, wxEXPAND, 5 );

	wxBoxSizer* bSizer2;
	bSizer2 = new wxBoxSizer( wxHORIZONTAL );

	land = new wxButton( this, wxID_ANY, _("Land Drone"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer2->Add( land, 1, wxALL, 5 );

	take_off = new wxButton( this, wxID_ANY, _("Take Off"), wxDefaultPosition, wxDefaultSize, 0 );
	bSizer2->Add( take_off, 1, wxALL, 5 );


	buttons->Add( bSizer2, 1, wxEXPAND, 5 );


	this->SetSizer( buttons );
	this->Layout();

	this->Centre( wxBOTH );
}

TelloGUI::~TelloGUI()
{
}
