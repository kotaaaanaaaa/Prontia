import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import { ThemeProvider } from "@mui/material/styles";
import * as React from "react";
import { fetchHistory } from "../../api/chat";
import type { ConversationResponse } from "../../api/dto";
import { HistoryTheme } from "./HistoryTheme";

const histories: ConversationResponse[] = await fetchHistory();
const History: React.FC = () => {
  const [history, setHistory] =
    React.useState<ConversationResponse[]>(histories);
  return (
    <div className="history">
      <ThemeProvider theme={HistoryTheme}>
        <List>
          {history.map((item) => (
            <ListItemButton key={item.id}>
              <ListItem>{item.title}</ListItem>
            </ListItemButton>
          ))}
        </List>
      </ThemeProvider>
    </div>
  );
};

export default History;
