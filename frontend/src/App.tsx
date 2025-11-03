import "./App.css";
import * as React from "react";
import { BrowserRouter, Route, Routes } from "react-router";
import SideMenu from "./components/SideMenu/SideMenu";
import MainContents from "./pages/MainContents";

function App() {
  const [open, setOpen] = React.useState(true);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route
            index
            element={
              <>
                <SideMenu open={open} setOpen={setOpen} />
                <MainContents open={open} />
              </>
            }
          />
          <Route
            path="/chat/:id"
            element={
              <>
                <SideMenu open={open} setOpen={setOpen} />
                <MainContents open={open} />
              </>
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
