import type * as React from "react";
import Chat from "./Chat";

const MainContents: React.FC<{ open: boolean }> = ({ open }) => {
  return (
    <div className="main-contents">
      <Chat />
    </div>
  );
};

export default MainContents;
