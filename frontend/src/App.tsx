import "./App.css";
import * as React from "react";
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
      <SideMenu open={open} setOpen={setOpen} />
      <MainContents open={open} />
    </div>
  );
}

export default App;
