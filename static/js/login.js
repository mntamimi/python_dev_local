        var app = new sap.m.App({
        });

        var oPage = new sap.m.Page({
            title: "SAP Products"
        });

        oVBox = new sap.m.VBox({});
        oVBox.setFitContainer(true);
        //oVBox.setJustifyContent("Center");
        oVBox.setAlignItems("Center");
        oVBox.setAlignContent("Center");
        var oNameInput = new sap.m.Input({
            type: sap.m.InputType.Text
        });
        var oNameLabel = new sap.m.Label({
            text: "User Name",
            labelFor: oNameInput
        });


        var oPasswordInput = new sap.m.Input({
            type: sap.m.InputType.Password
        });
        var oPasswordLabel = new sap.m.Label({
            text: "Password",
            labelFor: oPasswordInput
        });

        var oLogin = new sap.m.Button({
            text: 'Login',
            type: sap.m.ButtonType.Emphasized,
            press: function() {
                var oLoginData = {
                    "username": oNameInput.getValue(),
                    "password": oPasswordInput.getValue()
                };

                $.post("login", oLoginData, function(response) {
                    var oJsonResponse = JSON.parse(response);

                    if (oJsonResponse["Message"] === "") {
                        window.location.href = "/products";
                        //document.location.href = "/products";
                    } else {
                        if (!oJsonResponse["Message"])
                            oJsonResponse["Message"] = "Error";
                        var dialog = new sap.m.Dialog({
                            title: "Error",
                            type: "Message",
                            state: "Error",
                            content: new sap.m.Text({
                                text: oJsonResponse["Message"]
                            }),
                            beginButton: new sap.m.Button({
                                text: "OK",
                                press: function() {
                                    dialog.close();
                                }
                            }),
                            afterClose: function() {
                                dialog.destroy();
                            }
                        });
                        dialog.open();

                    }
                }.bind(this));

                /*
                    $.ajax({
                        url: "/login",
                        type: "POST",
                        beforeSend: function (req) {
                        req.setRequestHeader("Authorization",
                            "Basic " + btoa( oNameInput.getValue() + ":" + oPasswordInput.getValue()));
                        req.setRequestHeader("Access-Control-Allow-Origin", "*");
                            },

                        success: function (response) {
                            document.location.href = "/products";
                            },
                        error: function (error) {

                            oPasswordInput.setValue(null)
                            alert("Login Failed")
                            }
                    });
                    */
            }
        });

        oVBox.addItem(new sap.m.Label({
            text: "",
            design: sap.m.LabelDesign.Standard
        }).addStyleClass("login_subtitle"));
        oVBox.addItem(oNameLabel);
        oVBox.addItem(oNameInput);
        oVBox.addItem(oPasswordLabel);
        oVBox.addItem(oPasswordInput);
        oVBox.addItem(oLogin);
        oPage.addContent(oVBox);
        app.addPage(oPage);
        app.placeAt("content");
