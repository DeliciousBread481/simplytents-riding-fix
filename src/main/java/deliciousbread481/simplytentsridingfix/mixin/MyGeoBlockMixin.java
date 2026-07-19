package deliciousbread481.simplytentsridingfix.mixin;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.BlockPos;
import net.minecraft.world.phys.BlockHitResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(targets = "com.sappyeddie.simplytents.tent.block.MyGeoBlock", remap = false)
public class MyGeoBlockMixin {
    private static final Logger SIMPLYTENTSRIDINGFIX$LOGGER =
            LoggerFactory.getLogger("SimplyTentsRidingFix");

    @Inject(
        method = "m_6227_",
        at = @At("HEAD"),
        remap = false
    )
    private void simplytentsridingfix$logUseEntry(BlockState state, Level level, BlockPos pos,
                                                  Player player, InteractionHand hand, BlockHitResult hit,
                                                  CallbackInfoReturnable<InteractionResult> cir) {
        ItemStack stack = player.getItemInHand(hand);
        SIMPLYTENTSRIDINGFIX$LOGGER.info(
            "[SimplyTentsRidingFix] use() entry -> side={} isPassenger={} isCrouching={} emptyHand={} pos={}",
            (level.isClientSide ? "CLIENT" : "SERVER"),
            player.isPassenger(),
            player.isCrouching(),
            stack.isEmpty(),
            pos
        );
    }


    @Redirect(
        method = "m_6227_",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/entity/player/Player;m_6047_()Z"
        ),
        remap = false
    )
    private boolean simplytentsridingfix$allowPackWhileRiding(Player player) {
        return player.isCrouching() || player.isPassenger();
    }
}