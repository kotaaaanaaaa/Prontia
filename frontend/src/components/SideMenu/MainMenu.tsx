import EditSquareIcon from "@mui/icons-material/EditSquare";
import SearchIcon from "@mui/icons-material/Search";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import type { OverridableComponent } from "@mui/material/OverridableComponent";
import Stack from "@mui/material/Stack";
import type { SvgIconTypeMap } from "@mui/material/SvgIcon";
import { Link } from "react-router";

type SvgIconComponent = OverridableComponent<SvgIconTypeMap<{}, "svg">>;

const MenuButtonItem: React.FC<{
  expand: boolean;
  Icon: SvgIconComponent;
  text: string;
  link?: string;
}> = ({ expand, Icon, text, link }) => {
  const props = link
    ? {
        component: Link,
        to: link,
      }
    : {};

  return (
    <>
      {expand ? (
        <Button startIcon={<Icon />} {...props}>
          {text}
        </Button>
      ) : (
        <IconButton {...props}>{<Icon />}</IconButton>
      )}
    </>
  );
};

const MainMenu: React.FC<{ expand: boolean }> = ({ expand }) => {
  return (
    <div className="main-menu">
      <Stack direction="column">
        <MenuButtonItem
          expand={expand}
          Icon={EditSquareIcon}
          text="Edit"
          link="/"
        />
        <MenuButtonItem expand={expand} Icon={SearchIcon} text="Search" />
      </Stack>
    </div>
  );
};

export default MainMenu;
