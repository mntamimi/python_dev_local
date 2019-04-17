          var app = new sap.m.App({
        });

        var oPage = new sap.m.Page({
            title: "SAP Products"
        });

        oVBox = new sap.m.VBox({});
        oVBox.setFitContainer(true);
        //oVBox.setJustifyContent("Center");
        //oVBox.setAlignItems("Center");
        oVBox.setAlignContent("Center");

        var oNameInput = new sap.m.Input({
            type: sap.m.InputType.Text
        });

        this.oTableItems = [];
        var oGrid = new sap.ui.layout.VerticalLayout();
        var oVBox1 = new sap.m.VBox({});
        var oIdInput = new sap.m.Input({
            type: sap.m.InputType.Number
        });
        var oIdLabel = new sap.m.Label({
            text: "Product Id",
            labelFor: oIdInput
        });

        var oNameInput = new sap.m.Input({
            type: sap.m.InputType.Text
        });
        var oNameLabel = new sap.m.Label({
            text: "Product Name",
            labelFor: oNameInput
        });

        var oDescInput = new sap.m.Input({
            type: sap.m.InputType.Text
        });
        var oDescLabel = new sap.m.Label({
            text: "Product Description",
            labelFor: oDescInput
        });

        this.oTable = new sap.m.Table({
            id: "ProductsTable",
            items: this.oTableItems,
            columns: [
                new sap.m.Column({
                    header: [
                        new sap.m.Label({
                            text: "Product"
                        })
                    ]
                }), new sap.m.Column({
                    header: [
                        new sap.m.Label({
                            text: "Description"
                        })
                    ]
                }), new sap.m.Column({
                    header: [
                        new sap.m.Label({
                            text: "Price"
                        })
                    ]
                })
            ],

        });

        this.oTable.setInset(false);

        var oSearch = new sap.m.Button({
            text: 'Go',
            type: sap.m.ButtonType.Emphasized,
            press: function() {
                var oSearchData = {
                    "ProductId": oIdInput.getValue(),
                    "ProductName": oNameInput.getValue(),
                    "ProductDesc": oDescInput.getValue()
                };
                this.oTable.removeAllItems();
                $.post("products", oSearchData, function(response) {
                    this.oTableItems = JSON.parse(response).products;

                    for (var i = 0; i < this.oTableItems.length; i++) {
                        this.oTable.addItem(
                            new sap.m.ColumnListItem({
                                cells: [
                                    new sap.m.Text({
                                        text: this.oTableItems[i].productName
                                    }),
                                    new sap.m.Text({
                                        text: this.oTableItems[i].description
                                    }),
                                    new sap.m.Text({
                                        text: this.oTableItems[i].price
                                    })
                                ]
                            })
                        )
                    }
                }.bind(this));
            }.bind(this)
        });

        oVBox.addItem(new sap.m.Label({
            text: "",
            design: sap.m.LabelDesign.Standard
        }).addStyleClass("login_subtitle"));
        oVBox.addItem(oIdLabel);
        oVBox.addItem(oIdInput);
        oVBox.addItem(oNameLabel);
        oVBox.addItem(oNameInput);
        oVBox.addItem(oDescLabel);
        oVBox.addItem(oDescInput);
        oVBox.addItem(oSearch);
        oVBox.addItem(this.oTable);
        oPage.addContent(oVBox);
        app.addPage(oPage);
        app.placeAt("content");