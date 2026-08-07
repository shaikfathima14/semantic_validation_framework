import { Routes, Route } from "react-router-dom";

import LandingPage from "../pages/Landing/LandingPage";
import LoginPage from "../pages/Auth/LoginPage";
import RegisterPage from "../pages/Auth/RegisterPage";
import Dashboard from "../pages/Citizen/Dashboard";
import ScholarshipForm from "../pages/Scholarship/ScholarshipForm";
import IncomeForm from "../pages/Income/IncomeForm";
import ValidationReport from "../pages/Report/ValidationReport";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/scholarship" element={<ScholarshipForm />} />
      <Route path="/income" element={<IncomeForm />} />
      <Route path="/report" element={<ValidationReport />} />
    </Routes>
  );
}

export default AppRoutes;