import React from "react";
import { createRoot } from "react-dom/client";
import AgChart from "../components/ChartComponent";

// AG Grid Enterprise Setup
import { ModuleRegistry } from "ag-grid-community";
import { AllEnterpriseModule, LicenseManager } from "ag-grid-enterprise";

// Register ALL Enterprise modules
ModuleRegistry.registerModules([AllEnterpriseModule]);

// AG Grid Enterprise License Key Setup
LicenseManager.setLicenseKey("[TRIAL]_this_{AG_Charts_and_AG_Grid}_Enterprise_key_{AG-090575}_is_granted_for_evaluation_only___Use_in_production_is_not_permitted___Please_report_misuse_to_legal@ag-grid.com___For_help_with_purchasing_a_production_key_please_contact_info@ag-grid.com___You_are_granted_a_{Single_Application}_Developer_License_for_one_application_only___All_Front-End_JavaScript_developers_working_on_the_application_would_need_to_be_licensed___This_key_will_deactivate_on_{14 August 2025}____[v3]_[0102]_MTc1NTEyNjAwMDAwMA==2bf724e243e12a2673a0da27840ab6db");

const gridData: any = (window as any).gridData || [];

const container: HTMLElement = document.getElementById("root")!;
const root = createRoot(container);
root.render(<AgChart data={gridData} />);
