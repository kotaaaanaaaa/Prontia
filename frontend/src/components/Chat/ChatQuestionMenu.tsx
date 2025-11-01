import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import EditIcon from "@mui/icons-material/EditOutlined";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";

const ChatQuestionMenu: React.FC = () => {
  return (
    <Stack direction="row" justifyContent="flex-end">
      <IconButton>
        <ContentCopyIcon />
      </IconButton>
      <IconButton>
        <EditIcon />
      </IconButton>
    </Stack>
  );
};

export default ChatQuestionMenu;
