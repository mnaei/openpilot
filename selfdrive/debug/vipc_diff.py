import cv2

ROUTE1 = "https://commadataci.blob.core.windows.net/openpilotci/2f4452b03ccb98f0|2022-12-03--13-45-30_model_tici_0e0f55cf3bb2cf79b44adf190e6387a83deb6646.bz2"
ROUTE2 = "https://commadataci.blob.core.windows.net/openpilotci/2f4452b03ccb98f0|2022-12-03--13-45-30_model_tici_5e93a4a623e3e34a8a04618e307f5f5ce514de41.bz2"


fourcc = VideoWriter_fourcc(*'MP4V')
out = VideoWriter("diff.mp4", fourcc, 20.0, (256*2,256))


lr1 = logreader_from_ci_segment(ROUTE1)
lr2 = logreader_from_ci_segment(ROUTE2)


def im_from_nav_thumbnail(nav_thumbnail):
  return np.frombuffer(nav_thumbnail, dtype=np.uint8).reshape((256,256,3))


for m1, m2 in zip(lr1, lr2):
  assert m1.which() == m2.which()

  if m1.which() == "navThumbnail":
    m1_thumbnail = im_from_nav_thumbnail(m1.navThumbnail.thumbnail)
    m2_thumbnail = im_from_nav_thumbnail(m2.navThumbnail.thumbnail)
    
    combined = np.hstack(m1_thumbnail, m2_thumbnail)

    out.write(combined)

out.close()