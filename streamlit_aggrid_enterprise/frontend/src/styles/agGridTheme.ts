import {iconSetMaterial, themeQuartz} from 'ag-grid-community';

// to use myTheme in an application, pass it to the theme grid option
const myTheme = themeQuartz
    .withPart(iconSetMaterial)
	.withParams({
        // sideBarBackgroundColor: '#08f3',
        // sideButtonBarBackgroundColor: '#fff6',
        sideButtonBarTopPadding: 20,
        sideButtonSelectedUnderlineColor: 'orange',
        sideButtonTextColor: '#0009',
        sideButtonHoverBackgroundColor: '#fffa',
        sideButtonSelectedBackgroundColor: '#08f1',
        sideButtonHoverTextColor: '#000c',
        sideButtonSelectedTextColor: '#000e',
        sideButtonSelectedBorder: false,

        accentColor: "#087AD1",
        backgroundColor: "#FFFFFF",
        borderColor: "#D7E2E6",
        borderRadius: 2,
        browserColorScheme: "light",
        cellHorizontalPaddingScale: 0.7,
        chromeBackgroundColor: {
            ref: "backgroundColor"
        },
        columnBorder: false,
        fontFamily: {
            googleFont: "Inter"
        },
        fontSize: 12,
        foregroundColor: "#555B62",
        headerBackgroundColor: "#FFFFFF",
        headerFontSize: 13,
        headerFontWeight: 600,
        headerTextColor: "#000000",
        rowBorder: true,
        rowVerticalPaddingScale: 0.8,
        sidePanelBorder: true,
        spacing: 6,
        wrapperBorder: true,
        wrapperBorderRadius: 2
    });

export default myTheme;