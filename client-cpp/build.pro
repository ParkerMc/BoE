TEMPLATE = app
HEADERS = client_wss.hpp client_ws.hpp crypto.hpp ServerMan.h ui/main.h
SOURCES = main.cpp ui/main.cpp ServerMan.cpp
LIBS += -lboost_system -lpthread -lssl -lcrypto
