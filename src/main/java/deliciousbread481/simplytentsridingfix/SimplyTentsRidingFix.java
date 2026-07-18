package deliciousbread481.simplytentsridingfix;

import net.minecraftforge.fml.common.Mod;
import org.slf4j.Logger;
import com.mojang.logging.LogUtils;

@Mod(SimplyTentsRidingFix.MOD_ID)
public class SimplyTentsRidingFix {
    public static final String MOD_ID = "simplytentsridingfix";
    private static final Logger LOGGER = LogUtils.getLogger();

    public SimplyTentsRidingFix() {
        LOGGER.info("[SimplyTentsRidingFix] loaded - patching tent packing while riding");
    }
}