package deliciousbread481.simplytentsridingfix.mixin;

import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(targets = "com.sappyeddie.simplytents.tent.block.MyGeoBlock")
public class MyGeoBlockMixin {

    @Redirect(
        method = "use",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/entity/player/Player;isCrouching()Z"
        )
    )
    private boolean simplytentsridingfix$allowPackWhileRiding(Player player) {
        return player.isCrouching() || player.isPassenger();
    }
}0