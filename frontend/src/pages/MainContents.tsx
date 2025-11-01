import type * as React from "react";
import Chat from "../pages/Chat";

const MainContents: React.FC<{ open: boolean }> = ({ open }) => {
  return (
    <div className="main-contents">
      <Chat />
    </div>
  );
};

export default MainContents;
