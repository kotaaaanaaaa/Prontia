import "./App.css";
import * as React from "react";
import MainContents from "./MainContents";
import SideMenu from "./SideMenu";

function App() {
  const [open, setOpen] = React.useState(true);

  return (
    <>
      <SideMenu open={open} setOpen={setOpen} />
      <MainContents open={open} />
    </>
  );
}

export default App;
